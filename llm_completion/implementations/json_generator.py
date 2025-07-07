"""Implementation for generating data in JSON format based on schemas."""

from typing import Dict, List, Any, Optional, Union
import json

from ..completion import LiteLLMCompletion
from ..logger import logger


class JsonSchemaDataGenerator:
    """Generator for JSON data based on schemas."""

    def __init__(self, completion_provider: Optional[LiteLLMCompletion] = None) -> None:
        """Initialize the JSON generator.

        Args:
            completion_provider: Optional completion provider to use. If not provided,
                a new instance will be created.
        """
        self.completion_provider = completion_provider or LiteLLMCompletion()
        self.system_prompt = (
            "You are a data generation expert specializing in creating realistic "
            "JSON data that conforms to specific schemas."
        )

    def generate_data(
        self, 
        schemas: Union[Dict[str, Any], List[Dict[str, Any]]], 
        user_prompt: str,
        num_examples: int = 1
    ) -> List[Dict[str, Any]]:
        """Generate JSON data based on provided schemas.

        Args:
            schemas: JSON schema or list of schemas.
            user_prompt: Additional instructions for data generation.
            num_examples: Number of examples to generate.

        Returns:
            List of generated JSON data objects.

        Raises:
            Exception: If data generation fails.
        """
        logger.info(f"Generating data for {len(schemas) if isinstance(schemas, list) else 1} schemas")
        
        # Convert single schema to list for consistent handling
        if isinstance(schemas, dict):
            schemas_list = [schemas]
        else:
            schemas_list = schemas
            
        schemas_str = json.dumps(schemas_list, indent=2)
        
        prompt = (
            f"Generate {num_examples} examples of JSON data that conform to the following schema(s):\n\n"
            f"{schemas_str}\n\n"
            f"Additional requirements: {user_prompt}\n\n"
            "Return ONLY valid JSON data that matches the schema(s) provided. "
            "Format as a list of JSON objects, even if there's only one example."
        )

        try:
            result = self.completion_provider.complete_with_json(prompt, self.system_prompt)
            
            # Ensure result is a list
            if not isinstance(result, list):
                if isinstance(result, dict):
                    result = [result]
                else:
                    raise ValueError(f"Expected a list or dict, got {type(result)}")
            
            # Validate the data against schemas (basic validation)
            self._validate_data_against_schemas(result, schemas_list)
            
            logger.info(f"Successfully generated {len(result)} data examples")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to generate JSON data: {str(e)}")
            raise
            
    def _validate_data_against_schemas(
        self, data_list: List[Dict[str, Any]], schemas: List[Dict[str, Any]]
    ) -> None:
        """Basic validation of generated data against schemas.

        Args:
            data_list: List of generated data objects.
            schemas: List of JSON schemas.

        Raises:
            ValueError: If validation fails.
        """
        # Try using jsonschema if available
        try:
            import jsonschema
            has_jsonschema = True
        except ImportError:
            has_jsonschema = False
            logger.warning("jsonschema package not found. Skipping advanced schema validation.")
            
        # If we have multiple schemas but only one item, we might need to check
        # which schema it matches
        for data_item in data_list:
            if has_jsonschema:
                # Try each schema until one validates
                valid = False
                for schema in schemas:
                    try:
                        jsonschema.validate(data_item, schema)
                        valid = True
                        break
                    except jsonschema.exceptions.ValidationError:
                        continue
                
                if not valid:
                    logger.warning(f"Data item doesn't match any schema: {data_item}")
            else:
                # Basic validation: check required properties
                for schema in schemas:
                    if "required" in schema and isinstance(schema["required"], list):
                        for required_prop in schema["required"]:
                            if required_prop not in data_item:
                                logger.warning(f"Missing required property '{required_prop}' in data: {data_item}")