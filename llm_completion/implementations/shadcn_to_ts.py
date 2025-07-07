"""Implementation for converting Shadcn components to TypeScript."""

from typing import Dict, Any, Optional, Tuple
import json

from ..completion import LiteLLMCompletion
from ..logger import logger
from ..utils import extract_code_from_markdown


class ShadcnToTypeScriptConverter:
    """Converter for Shadcn React components to TypeScript."""

    def __init__(self, completion_provider: Optional[LiteLLMCompletion] = None) -> None:
        """Initialize the converter.

        Args:
            completion_provider: Optional completion provider to use. If not provided,
                a new instance will be created.
        """
        self.completion_provider = completion_provider or LiteLLMCompletion()
        self.system_prompt = (
            "You are a TypeScript expert specializing in React component conversion."
        )

    def convert(self, component_code: str) -> Tuple[str, str, Dict[str, Any]]:
        """Convert a Shadcn component to TypeScript.

        Args:
            component_code: The React component code to convert.

        Returns:
            Tuple containing (typescript_component, props_file_content, metadata)

        Raises:
            Exception: If the conversion fails.
        """
        logger.info("Converting Shadcn component to TypeScript")
        
        prompt = (
            "Convert following react component code to typescript compatible code with proper props types and export statement.\n"
            "Convert any button to anchor tag with href prop and make href a required prop.\n"
            "Extract the user visible things like Text, Button, URL, Image, etc as props. Ensure that the component is compatible with TypeScript and follows best practices for type definitions.\n"
            "Create Props in separate file.\n\n"
            f"{component_code}\n\n"
            "Also give json for component name and component props name in following format,\n\n"
            "{\n"
            '"name": "<component name>",\n'
            '"props": "<component props name>",\n'
            '"props_file_name": "<component props file name>"\n'
            "}\n"
        )

        try:
            result = self.completion_provider.complete(prompt, self.system_prompt)
            
            # Extract the TypeScript component code
            ts_component_code = extract_code_from_markdown(result, "tsx")
            if not ts_component_code:
                ts_component_code = extract_code_from_markdown(result, "typescript")
            if not ts_component_code:
                ts_component_code = extract_code_from_markdown(result, "ts")
            
            # Extract the Props file content
            props_file_content = extract_code_from_markdown(result, "ts")
            
            # Extract the JSON metadata
            metadata_str = extract_code_from_markdown(result, "json")
            if not metadata_str:
                # Try to find JSON content without code block
                import re
                json_pattern = r'\{[\s\S]*?"name"[\s\S]*?"props"[\s\S]*?"props_file_name"[\s\S]*?\}'
                match = re.search(json_pattern, result)
                if match:
                    metadata_str = match.group(0)
            
            # Parse JSON metadata
            try:
                metadata = json.loads(metadata_str) if metadata_str else {}
            except json.JSONDecodeError:
                logger.warning("Failed to parse metadata JSON, using empty dict")
                metadata = {}
            
            # Validate results
            if not ts_component_code:
                raise ValueError("Failed to extract TypeScript component code")
                
            logger.info("Successfully converted component to TypeScript")
            
            return ts_component_code, props_file_content, metadata
            
        except Exception as e:
            logger.error(f"Failed to convert component to TypeScript: {str(e)}")
            raise