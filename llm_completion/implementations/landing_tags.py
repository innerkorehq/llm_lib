"""Implementation for finding tags for landing pages."""

from typing import List, Optional
import json

from ..completion import LiteLLMCompletion
from ..logger import logger


class LandingPageTagFinder:
    """Component tag finder for landing pages."""

    def __init__(self, completion_provider: Optional[LiteLLMCompletion] = None) -> None:
        """Initialize the tag finder.

        Args:
            completion_provider: Optional completion provider to use. If not provided,
                a new instance will be created.
        """
        self.completion_provider = completion_provider or LiteLLMCompletion()
        self.system_prompt = (
            "You are a UI/UX expert specializing in landing page design."
        )

    def find_tags(self, components: List[str], count: int = 5) -> List[str]:
        """Find appropriate tags for a landing page from a list of components.

        Args:
            components: List of available component names.
            count: Minimum number of components to select.

        Returns:
            List of selected component tags.

        Raises:
            Exception: If tag finding fails.
        """
        logger.info(f"Finding landing page tags from {len(components)} components")
        
        prompt = (
            f"As a UI/UX expert, select at least {count} components in sequence for a landing page from the following list.\n"
            "Choose components that work well together for a modern, effective landing page.\n"
            "Format your response as a JSON array of strings containing only component names.\n\n"
            f"Available components: {json.dumps(components)}\n\n"
            "Remember to:\n"
            f"1. Select at least {count} components\n"
            "2. Choose components that logically work together\n"
            "3. Return only a valid JSON array of component names\n\n"
            "JSON array:"
        )

        try:
            result = self.completion_provider.complete_with_json(prompt, self.system_prompt)
            
            if not isinstance(result, list):
                logger.warning("Result is not a list, attempting to extract list from response")
                if isinstance(result, dict) and any(isinstance(result.get(k), list) for k in result):
                    # Try to find a list in the dictionary
                    for k, v in result.items():
                        if isinstance(v, list):
                            result = v
                            break
                else:
                    raise ValueError(f"Expected a list, got {type(result)}")
            
            # Validate that the result contains strings
            tags = [str(item) for item in result]
            
            # Ensure minimum number of components
            if len(tags) < count:
                logger.warning(f"Got only {len(tags)} tags, but requested {count}. Adding defaults.")
                default_components = ["Hero", "Features", "Testimonials", "CTA", "Footer"]
                for c in default_components:
                    if c not in tags and len(tags) < count:
                        tags.append(c)
            
            logger.info(f"Found {len(tags)} landing page tags")
            
            return tags
            
        except Exception as e:
            logger.error(f"Failed to find landing page tags: {str(e)}")
            raise