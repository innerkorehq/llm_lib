"""Implementation for converting Shadcn components to TypeScript."""

from typing import Dict, Any, Optional, Tuple
import json
import re

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

    def convert(self, component_code: str) -> Dict[str, Any]:
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
            "Extract the user visible things like Text, Button, URL, Image, etc as props. \n"
            "Ensure that the component is compatible with TypeScript and follows best practices for type definitions.\n"
            "Create Props in same file.\n"
            "Handle Icons properly - if component uses icons, make sure they're imported from react-icons packages.\n\n"
            f"{component_code}\n\n"
            "Give only json for component ts code, component name, props_file_name and component props name in following format,\n\n"
            "{\n"
            '"name": "<component name>",\n'
            '"component_ts_code": "<component ts code>",\n'
            '"props": "<component props name>",\n'
            '"props_file_name": "<component props file name>"\n'
            "}\n"
        )

        try:
            result = self.completion_provider.complete_with_json(prompt, self.system_prompt)
            
            logger.info("Successfully converted component to TypeScript")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to convert component to TypeScript: {str(e)}")
            raise
    
    def _extract_props_from_component(self, component_code: str, metadata: Dict[str, Any]) -> str:
        """Extract props interface from component code if props file is missing.

        Args:
            component_code: TypeScript component code.
            metadata: Component metadata.

        Returns:
            Props file content.
        """
        try:
            # Try to find props interface in the component
            props_pattern = r"(export\s+)?interface\s+(\w+Props)\s*\{[\s\S]+?\}"
            props_match = re.search(props_pattern, component_code)
            
            if props_match:
                props_content = props_match.group(0)
                props_name = props_match.group(2)
                
                # Update metadata if props name is missing
                if "props" not in metadata:
                    metadata["props"] = props_name
                
                return f"export {props_content}"
            
            # If no props interface found, create a basic one based on metadata
            props_name = metadata.get("props", "ComponentProps")
            return f"export interface {props_name} {{\n  children?: React.ReactNode;\n}}"
            
        except Exception as e:
            logger.warning(f"Error extracting props from component: {str(e)}")
            props_name = metadata.get("props", "ComponentProps")
            return f"export interface {props_name} {{\n  children?: React.ReactNode;\n}}"