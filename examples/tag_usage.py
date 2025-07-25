"""Examples of tag functionality in the LLM completion library."""

import sys
import os
import json
from typing import List, Dict, Any

# Add parent directory to path for direct import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from llm_completion.tag_manager import TagManager
    from llm_completion.implementations.landing_tags import LandingPageTagFinder
except ImportError as e:
    print(f"Error importing library: {e}")
    print("Make sure the library is installed or in PYTHONPATH")
    sys.exit(1)


def print_section(title: str) -> None:
    """Print a section header.
    
    Args:
        title: Section title.
    """
    print("\n" + "=" * 50)
    print(f" {title} ".center(50, "="))
    print("=" * 50)


def example_tag_search() -> None:
    """Demonstrate tag search functionality."""
    print_section("Tag Search Example")
    
    tag_manager = TagManager()
    
    # Search for tags
    queries = ["hero", "conversion", "mobile", "action"]
    
    for query in queries:
        results = tag_manager.search_tags(query)
        print(f"Tags matching '{query}':")
        for tag in results:
            print(f"  - {tag}")
        print()


def example_component_recommendations() -> None:
    """Demonstrate component recommendation functionality."""
    print_section("Component Recommendations Example")
    
    tag_finder = LandingPageTagFinder(use_api=False)
    
    # Get different focus areas
    focus_areas = [None, "conversion", "trust", "awareness", "engagement"]
    
    for focus in focus_areas:
        components = tag_finder.tag_manager.get_component_combinations(count=5, focus=focus)
        focus_name = focus if focus else "general"
        print(f"Recommended components for '{focus_name}' focus:")
        for i, component in enumerate(components):
            print(f"  {i+1}. {component}")
        print()


def example_component_tagging() -> None:
    """Demonstrate component tagging functionality."""
    print_section("Component Tagging Example")
    
    tag_finder = LandingPageTagFinder(use_api=False)
    
    # Get tags for different components
    components = ["Hero", "PricingTable", "TestimonialSlider", "ContactForm", "FeatureGrid"]
    
    for component in components:
        tags = tag_finder.get_tags_for_component(component)
        print(f"Tags for '{component}':")
        print(f"  Primary: {tags['primary']}")
        print(f"  All tags: {', '.join(tags['tags'])}")
        print()


def example_page_analysis() -> None:
    """Demonstrate page analysis functionality."""
    print_section("Page Analysis Example")
    
    tag_finder = LandingPageTagFinder(use_api=False)
    
    # Example component structure
    components = [
        {"name": "Hero", "type": "section"},
        {"name": "Features", "type": "grid"},
        {"name": "Testimonials", "type": "slider"},
        {"name": "Pricing", "type": "cards"},
        {"name": "Contact", "type": "form"}
    ]
    
    # Analyze the structure
    analysis = tag_finder.analyze_component_structure(components)
    
    print("Landing page analysis:")
    print(json.dumps(analysis, indent=2))
    print()
    
    # Example of incomplete structure
    incomplete = [
        {"name": "Hero", "type": "section"},
        {"name": "Features", "type": "grid"}
    ]
    
    incomplete_analysis = tag_finder.analyze_component_structure(incomplete)
    
    print("Incomplete landing page analysis:")
    print(json.dumps(incomplete_analysis, indent=2))


def main() -> None:
    """Run tag functionality examples."""
    print("LLM Completion Library - Tag Functionality Examples")
    
    try:
        # Run examples
        example_tag_search()
        example_component_recommendations()
        example_component_tagging()
        example_page_analysis()
        
    except Exception as e:
        print(f"Error running examples: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()