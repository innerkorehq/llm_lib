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
            "Fill image assets with Unsplash stock images you know exist.\n"
            "Use icons for svgs or logos if component requires them. Return icons as a JSON dict with "
            "fields 'package' (react-icons package name) and 'name' (icon name), e.g., "
            "{'package': 'react-icons/fa', 'name': 'FaUser'}. Only use known icons from react-icons.\n\n"
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
            
            # Process the data to ensure all image and icon fields are properly formatted
            processed_result = self._process_generated_data(result)
            
            logger.info(f"Successfully generated {len(processed_result)} data examples")
            
            return processed_result
            
        except Exception as e:
            logger.error(f"Failed to generate JSON data: {str(e)}")
            raise
    
    def _process_generated_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process generated data to ensure proper formatting for images and icons.

        Args:
            data: List of generated data objects.

        Returns:
            List of processed data objects.
        """
        processed_data = []
        
        for item in data:
            processed_item = self._process_item(item)
            processed_data.append(processed_item)
            
        return processed_data
    
    def _process_item(self, item: Any) -> Any:
        """Recursively process an item to format images and icons.

        Args:
            item: Data item to process.

        Returns:
            Processed data item.
        """
        if isinstance(item, dict):
            # Process each key-value pair
            processed_item = {}
            for key, value in item.items():
                processed_value = self._process_item(value)
                
                # Special handling for keys that might contain images or icons
                if isinstance(processed_value, str):
                    # Check if it's potentially an image URL
                    if any(img_key in key.lower() for img_key in ["image", "img", "photo", "picture", "thumbnail"]):
                        if not processed_value.startswith("http"):
                            processed_value = self._ensure_unsplash_url(processed_value, key)
                    
                    # Check if it's potentially an icon
                    elif any(icon_key in key.lower() for icon_key in ["icon", "svg", "logo"]):
                        if not isinstance(processed_value, dict) and not processed_value.startswith("http"):
                            processed_value = self._format_icon(processed_value)
                
                processed_item[key] = processed_value
            return processed_item
            
        elif isinstance(item, list):
            # Process each item in the list
            return [self._process_item(subitem) for subitem in item]
            
        else:
            # Return primitive types unchanged
            return item
    
    def _ensure_unsplash_url(self, value: str, context: str = "") -> str:
        """Ensure a value is a proper Unsplash URL if it's meant to be an image.

        Args:
            value: The potential image value.
            context: Context information for better image selection.

        Returns:
            Properly formatted Unsplash URL.
        """
        if value.startswith("http") and "unsplash.com" in value:
            return value
            
        # Create a reasonable Unsplash URL based on the value
        sanitized = value.replace(" ", "-").lower()
        # If it's just a placeholder, use context to create better URL
        if value in ["image", "placeholder", "photo"] and context:
            sanitized = context.lower()
            
        return f"https://source.unsplash.com/random?{sanitized}"
    
    def _format_icon(self, value: str) -> Dict[str, str]:
        """Format an icon string into a proper react-icons object.

        Args:
            value: Icon string to format.

        Returns:
            Formatted icon object.
        """
        # If already formatted properly, return as is
        if isinstance(value, dict) and "package" in value and "name" in value:
            return value
            
        # Try to determine icon type from prefix
        value = value.strip()
        icon_name = value
        
        # If it doesn't start with a capital letter, capitalize and prefix with package abbreviation
        if not (value and value[0].isupper()):
            # Default to Font Awesome
            icon_name = f"Fa{value.capitalize()}"
        
        # Determine package based on prefix
        package = "react-icons/fa"  # Default to Font Awesome
        if icon_name.startswith("Fa"):
            package = "react-icons/fa"
        elif icon_name.startswith("Md"):
            package = "react-icons/md"
        elif icon_name.startswith("Io"):
            package = "react-icons/io"
        elif icon_name.startswith("Bi"):
            package = "react-icons/bi"
        elif icon_name.startswith("Fi"):
            package = "react-icons/fi"
        
        return {
            "package": package,
            "name": icon_name
        }