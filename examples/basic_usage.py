"""Basic usage examples for the LLM completion library."""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path for direct import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from llm_completion import LiteLLMCompletion
    from llm_completion.implementations import (
        ShadcnToTypeScriptConverter,
        LandingPageTagFinder,
        JsonSchemaDataGenerator,
    )
    from llm_completion.exceptions import CompletionError, APIKeyError
except ImportError as e:
    print(f"Error importing library: {e}")
    print("Make sure the library is installed or in PYTHONPATH")
    sys.exit(1)


def main():
    """Run basic examples of the LLM completion library."""
    # Load environment variables
    load_dotenv()
    
    try:
        # Check for API keys
        if not os.getenv("GEMINI_API_KEY") and not os.getenv("OPENAI_API_KEY"):
            print("ERROR: No API keys found! Please set GEMINI_API_KEY or OPENAI_API_KEY in environment variables")
            sys.exit(1)
    
        # Basic completion example
        print("\n===== Basic Completion =====")
        completion = LiteLLMCompletion()
        # result = completion.complete("Explain quantum computing in simple terms")
        # print(result)
        
        # JSON completion example
        print("\n===== JSON Completion =====")
        # json_result = completion.complete_with_json(
        #     "List 3 planets in our solar system with their key features"
        # )
        # print(json_result)
        
        # Shadcn to TypeScript example
        print("\n===== Shadcn to TypeScript =====")
        converter = ShadcnToTypeScriptConverter()
        component_code = """
        import { useEffect, useMemo, useState } from \"react\";\nimport { motion } from \"framer-motion\";\nimport { MoveRight, PhoneCall } from \"lucide-react\";\nimport { Button } from \"@/components/ui/button\";\n\nfunction Hero() {\n  const [titleNumber, setTitleNumber] = useState(0);\n  const titles = useMemo(\n    () =\u003E [\"amazing\", \"new\", \"wonderful\", \"beautiful\", \"smart\"],\n    []\n  );\n\n  useEffect(() =\u003E {\n    const timeoutId = setTimeout(() =\u003E {\n      if (titleNumber === titles.length - 1) {\n        setTitleNumber(0);\n      } else {\n        setTitleNumber(titleNumber + 1);\n      }\n    }, 2000);\n    return () =\u003E clearTimeout(timeoutId);\n  }, [titleNumber, titles]);\n\n  return (\n    \u003Cdiv className=\"w-full\"\u003E\n      \u003Cdiv className=\"container mx-auto\"\u003E\n        \u003Cdiv className=\"flex gap-8 py-20 lg:py-40 items-center justify-center flex-col\"\u003E\n          \u003Cdiv\u003E\n            \u003CButton variant=\"secondary\" size=\"sm\" className=\"gap-4\"\u003E\n              Read our launch article \u003CMoveRight className=\"w-4 h-4\" /\u003E\n            \u003C/Button\u003E\n          \u003C/div\u003E\n          \u003Cdiv className=\"flex gap-4 flex-col\"\u003E\n            \u003Ch1 className=\"text-5xl md:text-7xl max-w-2xl tracking-tighter text-center font-regular\"\u003E\n              \u003Cspan className=\"text-spektr-cyan-50\"\u003EThis is something\u003C/span\u003E\n              \u003Cspan className=\"relative flex w-full justify-center overflow-hidden text-center md:pb-4 md:pt-1\"\u003E\n                &nbsp;\n                {titles.map((title, index) =\u003E (\n                  \u003Cmotion.span\n                    key={index}\n                    className=\"absolute font-semibold\"\n                    initial={{ opacity: 0, y: \"-100\" }}\n                    transition={{ type: \"spring\", stiffness: 50 }}\n                    animate={\n                      titleNumber === index\n                        ? {\n                            y: 0,\n                            opacity: 1,\n                          }\n                        : {\n                            y: titleNumber \u003E index ? -150 : 150,\n                            opacity: 0,\n                          }\n                    }\n                  \u003E\n                    {title}\n                  \u003C/motion.span\u003E\n                ))}\n              \u003C/span\u003E\n            \u003C/h1\u003E\n\n            \u003Cp className=\"text-lg md:text-xl leading-relaxed tracking-tight text-muted-foreground max-w-2xl text-center\"\u003E\n              Managing a small business today is already tough. Avoid further\n              complications by ditching outdated, tedious trade methods. Our\n              goal is to streamline SMB trade, making it easier and faster than\n              ever.\n            \u003C/p\u003E\n          \u003C/div\u003E\n          \u003Cdiv className=\"flex flex-row gap-3\"\u003E\n            \u003CButton size=\"lg\" className=\"gap-4\" variant=\"outline\"\u003E\n              Jump on a call \u003CPhoneCall className=\"w-4 h-4\" /\u003E\n            \u003C/Button\u003E\n            \u003CButton size=\"lg\" className=\"gap-4\"\u003E\n              Sign up here \u003CMoveRight className=\"w-4 h-4\" /\u003E\n            \u003C/Button\u003E\n          \u003C/div\u003E\n        \u003C/div\u003E\n      \u003C/div\u003E\n    \u003C/div\u003E\n  );\n}\n\nexport { Hero };\n
        """
        ts_component, props_file, metadata = converter.convert(component_code)
        print("TypeScript Component:")
        print(ts_component)
        print("\nProps File:")
        print(props_file)
        print("\nMetadata:")
        print(metadata)
        
        # Landing page tags example
        print("\n===== Landing Page Tags =====")
        tag_finder = LandingPageTagFinder()
        components = ["Hero", "Features", "Pricing", "Testimonials", "FAQ", "CTA", "Footer", "Navbar"]
        tags = tag_finder.find_tags(components, count=5)
        print(tags)
        
        # JSON generator example
        print("\n===== JSON Generator =====")
        generator = JsonSchemaDataGenerator()
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer", "minimum": 18, "maximum": 100},
                "email": {"type": "string", "format": "email"}
            },
            "required": ["name", "email"]
        }
        data = generator.generate_data(
            schema,
            "Create profiles for tech industry professionals",
            num_examples=2
        )
        print(data)
    
    except APIKeyError as e:
        print(f"API Key Error: {str(e)}")
        print("Please set up valid API keys in your environment variables.")
    
    except CompletionError as e:
        print(f"Completion Error: {str(e)}")
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()