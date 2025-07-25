"""Example of component processing in the LLM completion library."""

import sys
import os
import json

# Add parent directory to path for direct import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from llm_completion.component_processor import ComponentProcessor
except ImportError as e:
    print(f"Error importing library: {e}")
    print("Make sure the library is installed or in PYTHONPATH")
    sys.exit(1)


# Example shadcn component
EXAMPLE_COMPONENT = """
function Button({ children, onClick }) {
  return (
    <button 
      className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
      onClick={onClick}
    >
      {children}
    </button>
  )
}

export default Button
"""

# Another example with icons
EXAMPLE_COMPONENT_WITH_ICON = """
import { ChevronRight } from "lucide-react"

function FeatureCard({ title, description, icon }) {
  return (
    <div className="p-6 border rounded-lg shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center mb-4">
        {icon || <ChevronRight className="h-5 w-5 mr-2 text-blue-500" />}
        <h3 className="text-lg font-medium">{title}</h3>
      </div>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}

export default FeatureCard
"""


def process_example_component():
    """Process an example shadcn component."""
    print("Processing example Button component...")
    
    # Create a processor
    processor = ComponentProcessor()
    
    # Process the component
    result = processor.process_component(EXAMPLE_COMPONENT, "Button.jsx")
    
    # Print the result
    print("\nProcessing result:")
    print(json.dumps(result, indent=2))
    
    # For demonstration, also save the files
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    component_path = os.path.join(output_dir, result["component"]["file_name"])
    props_path = os.path.join(output_dir, result["props"]["file_name"])
    metadata_path = os.path.join(output_dir, "button_metadata.json")
    
    with open(component_path, "w") as f:
        f.write(result["component"]["typescript_code"])
        
    with open(props_path, "w") as f:
        f.write(result["props"]["code"])
        
    with open(metadata_path, "w") as f:
        json.dump(result, f, indent=2)
        
    print(f"\nFiles saved to {output_dir}")


def process_component_with_icon():
    """Process an example component with icons."""
    print("\nProcessing example FeatureCard component with icons...")
    
    # Create a processor
    processor = ComponentProcessor()
    
    # Process the component
    result = processor.process_component(EXAMPLE_COMPONENT_WITH_ICON, "FeatureCard.jsx")
    
    # Print the result
    print("\nProcessing result:")
    print(json.dumps(result, indent=2))
    
    # For demonstration, also save the files
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    component_path = os.path.join(output_dir, result["component"]["file_name"])
    props_path = os.path.join(output_dir, result["props"]["file_name"])
    metadata_path = os.path.join(output_dir, "feature_card_metadata.json")
    
    with open(component_path, "w") as f:
        f.write(result["component"]["typescript_code"])
        
    with open(props_path, "w") as f:
        f.write(result["props"]["code"])
        
    with open(metadata_path, "w") as f:
        json.dump(result, f, indent=2)
        
    print(f"\nFiles saved to {output_dir}")


def main():
    """Run component processing examples."""
    print("LLM Completion Library - Component Processing Example")
    
    try:
        # Check for API keys
        if not os.getenv("GEMINI_API_KEY") and not os.getenv("OPENAI_API_KEY"):
            print("ERROR: No API keys found! Please set GEMINI_API_KEY or OPENAI_API_KEY environment variables")
            sys.exit(1)
            
        # Process example components
        process_example_component()
        process_component_with_icon()
        
    except Exception as e:
        print(f"Error in example: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()