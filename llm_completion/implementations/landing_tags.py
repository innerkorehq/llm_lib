"""Implementation for finding tags for landing pages."""

from typing import List, Optional, Dict, Any
import json

from ..completion import LiteLLMCompletion
from ..logger import logger
from ..tag_manager import TagManager


class LandingPageTagFinder:
    """Component tag finder for landing pages."""

    def __init__(
        self, 
        completion_provider: Optional[LiteLLMCompletion] = None,
        use_api: bool = False
    ) -> None:
        """Initialize the tag finder.

        Args:
            completion_provider: Optional completion provider to use when API is needed.
                If not provided and use_api is True, a new instance will be created.
            use_api: Whether to use the API for tag finding or use built-in tag data.
        """
        self.use_api = use_api
        if use_api:
            self.completion_provider = completion_provider or LiteLLMCompletion()
        
        # Initialize the tag manager for local tag operations
        self.tag_manager = TagManager()
        
        self.system_prompt = (
            "You are a UI/UX expert specializing in landing page design."
        )

    def find_tags(
        self, 
        components: List[str], 
        count: int = 9,
        focus: Optional[str] = None
    ) -> List[str]:
        """Find appropriate tags for a landing page from a list of components.

        Args:
            components: List of available component names.
            count: Minimum number of components to select.
            focus: Optional focus area (e.g., 'conversion', 'trust').

        Returns:
            List of selected component tags.

        Raises:
            Exception: If tag finding fails.
        """
        logger.info(f"Finding landing page tags from {len(components)} components")
        
        if not components:
            logger.warning("Empty components list provided, using default recommendations")
            return self.tag_manager.get_component_combinations(count, focus)
        
        if not self.use_api:
            # Use local tag manager to determine component selection
            # First check if we have exact components in our list
            available_components = set(components)
            recommended = self.tag_manager.get_component_combinations(count, focus)
            
            # Filter recommended components to only those available
            filtered = [c for c in recommended if c in available_components]
            
            # If we don't have enough, add others from the available list
            if len(filtered) < count and len(components) >= count:
                remaining = [c for c in components if c not in filtered]
                filtered.extend(remaining[:count - len(filtered)])
                
            return filtered[:count]
        
        # Use API approach if explicitly requested
        try:
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

            result = self.completion_provider.complete_with_json(prompt, self.system_prompt)
            
            if not isinstance(result, list):
                logger.warning("API result is not a list, attempting to extract list from response")
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
                logger.warning(f"API returned only {len(tags)} tags, but requested {count}. Adding defaults.")
                default_components = self.tag_manager.get_component_combinations(count - len(tags))
                for c in default_components:
                    if c not in tags and len(tags) < count:
                        tags.append(c)
            
            logger.info(f"Found {len(tags)} landing page tags via API")
            
            return tags
            
        except Exception as e:
            logger.error(f"API approach failed for finding landing page tags: {str(e)}")
            # Fallback to local approach
            logger.info("Falling back to local tag recommendations")
            return self.tag_manager.get_component_combinations(count, focus)
    
    def get_tags_for_component(
        self, 
        component_name: str, 
        additional_count: int = 4
    ) -> Dict[str, Any]:
        """Get appropriate tags for a specific component.

        Args:
            component_name: Name of the component.
            additional_count: Number of additional tags to include.

        Returns:
            Dictionary with primary tag and recommended tags.
        """
        try:
            recommended = self.tag_manager.get_recommended_tags(component_name)
            
            if not recommended:
                # No predefined tags, create a balanced set
                primary = component_name.lower()
                all_tags = self.tag_manager.create_tag_set(primary, additional_count)
                return {
                    "primary": primary,
                    "tags": all_tags
                }
            
            return {
                "primary": recommended[0],
                "tags": recommended
            }
            
        except Exception as e:
            logger.error(f"Error getting tags for component '{component_name}': {str(e)}")
            return {
                "primary": component_name.lower(),
                "tags": [component_name.lower()]
            }
    
    def analyze_component_structure(self, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the structure of components in a landing page.

        Args:
            components: List of component objects with at least a 'name' field.

        Returns:
            Analysis information about the landing page structure.
        """
        try:
            # Track tag usage
            tag_usage = {}
            category_coverage = {category: 0 for category in self.tag_manager.TAG_CATEGORIES}
            missing_categories = []
            
            # Check each component
            for component in components:
                name = component.get("name", "")
                if not name:
                    continue
                    
                tags = self.tag_manager.get_recommended_tags(name)
                
                # Update tag usage
                for tag in tags:
                    tag_usage[tag] = tag_usage.get(tag, 0) + 1
                    
                    # Update category coverage
                    for category, category_tags in self.tag_manager.TAG_CATEGORIES.items():
                        if tag in category_tags:
                            category_coverage[category] += 1
            
            # Find missing categories
            for category, count in category_coverage.items():
                if count == 0:
                    missing_categories.append(category)
            
            # Analyze structure
            has_hero = any(comp.get("name", "").lower() == "hero" for comp in components)
            has_cta = any(comp.get("name", "").lower() == "cta" for comp in components)
            has_footer = any(comp.get("name", "").lower() == "footer" for comp in components)
            
            # Generate suggestions
            suggestions = []
            if not has_hero:
                suggestions.append("Add a Hero section at the top of your landing page")
            if not has_cta:
                suggestions.append("Include a Call to Action (CTA) section")
            if not has_footer:
                suggestions.append("Add a Footer section")
                
            if missing_categories:
                for category in missing_categories:
                    if category in ["primary", "function", "content"]:
                        suggestions.append(f"Add components with '{category}' tags for better balance")
            
            return {
                "component_count": len(components),
                "has_essential_sections": {
                    "hero": has_hero,
                    "cta": has_cta,
                    "footer": has_footer
                },
                "category_coverage": category_coverage,
                "missing_categories": missing_categories,
                "suggestions": suggestions
            }
            
        except Exception as e:
            logger.error(f"Error analyzing component structure: {str(e)}")
            return {
                "component_count": len(components),
                "error": str(e)
            }