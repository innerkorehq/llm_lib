"""Basic usage examples for the LLM completion library."""

import os
import sys
import json
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
        
        # JSON completion with schema example
        print("\n===== JSON Completion with Schema =====")
        schema = {
            "type": "object",
            "properties": {
                "planets": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "diameter_km": {"type": "number"},
                            "has_rings": {"type": "boolean"},
                            "description": {"type": "string"}
                        },
                        "required": ["name", "diameter_km", "has_rings"]
                    }
                }
            },
            "required": ["planets"]
        }
        
        # Uncomment to run example
        # json_result_with_schema = completion.complete_with_json(
        #     "List 3 planets in our solar system with their key features",
        #     json_schema=schema
        # )
        # print(json.dumps(json_result_with_schema, indent=2))
        
        # Shadcn to TypeScript example
        print("\n===== Shadcn to TypeScript =====")
        converter = ShadcnToTypeScriptConverter()
        component_code = """
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Mockup } from "@/components/ui/mockup"
import { Glow } from "@/components/ui/glow"

interface HeroWithMockupProps {
  title: string
  description: string
  primaryCta?: {
    text: string
    href: string
  }
  secondaryCta?: {
    text: string
    href: string
    icon?: React.ReactNode
  }
  mockupImage: {
    src: string
    alt: string
    width: number
    height: number
  }
  className?: string
}
        # The ShadcnToTypeScriptConverter internally uses complete_with_json with json_schema
        # to ensure consistent TypeScript interface generation
        # result = converter.convert(component_code)
        # print("Results are:")
        # print(json.dumps(result, indent=2))

export function HeroWithMockup({
  title,
  description,
  primaryCta = {
    text: "Get Started",
    href: "/get-started",
  },
  secondaryCta = {
    text: "GitHub",
    href: "https://github.com/your-repo",
    icon: <GitHubIcon className="mr-2 h-4 w-4" />,
  },
  mockupImage,
  className,
}: HeroWithMockupProps) {
  return (
    <section
      className={cn(
        "relative bg-background text-foreground",
        "py-12 px-4 md:py-24 lg:py-32",
        "overflow-hidden",
        className,
      )}
    >
      <div className="relative mx-auto max-w-[1280px] flex flex-col gap-12 lg:gap-24">
        <div className="relative z-10 flex flex-col items-center gap-6 pt-8 md:pt-16 text-center lg:gap-12">
          {/* Heading */}
          <h1
            className={cn(
              "inline-block animate-appear",
              "bg-gradient-to-b from-foreground via-foreground/90 to-muted-foreground",
              "bg-clip-text text-transparent",
              "text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl",
              "leading-[1.1] sm:leading-[1.1]",
              "drop-shadow-sm dark:drop-shadow-[0_0_15px_rgba(255,255,255,0.1)]",
            )}
          >
            {title}
          </h1>

          {/* Description */}
          <p
            className={cn(
              "max-w-[550px] animate-appear opacity-0 [animation-delay:150ms]",
              "text-base sm:text-lg md:text-xl",
              "text-muted-foreground",
              "font-medium",
            )}
          >
            {description}
          </p>

          {/* CTAs */}
          <div
            className="relative z-10 flex flex-wrap justify-center gap-4 
            animate-appear opacity-0 [animation-delay:300ms]"
          >
            <Button
              asChild
              size="lg"
              className={cn(
                "bg-gradient-to-b from-brand to-brand/90 dark:from-brand/90 dark:to-brand/80",
                "hover:from-brand/95 hover:to-brand/85 dark:hover:from-brand/80 dark:hover:to-brand/70",
                "text-white shadow-lg",
                "transition-all duration-300",
              )}
            >
              <a href={primaryCta.href}>{primaryCta.text}</a>
            </Button>

            <Button
              asChild
              size="lg"
              variant="ghost"
              className={cn(
                "text-foreground/80 dark:text-foreground/70",
                "transition-all duration-300",
              )}
            >
              <a href={secondaryCta.href}>
                {secondaryCta.icon}
                {secondaryCta.text}
              </a>
            </Button>
          </div>

          {/* Mockup */}
          <div className="relative w-full pt-12 px-4 sm:px-6 lg:px-8">
            <Mockup
              className={cn(
                "animate-appear opacity-0 [animation-delay:700ms]",
                "shadow-[0_0_50px_-12px_rgba(0,0,0,0.3)] dark:shadow-[0_0_50px_-12px_rgba(255,255,255,0.1)]",
                "border-brand/10 dark:border-brand/5",
              )}
            >
              <img
                {...mockupImage}
                className="w-full h-auto"
                loading="lazy"
                decoding="async"
              />
            </Mockup>
          </div>
        </div>
      </div>

      {/* Background Glow */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <Glow
          variant="above"
          className="animate-appear-zoom opacity-0 [animation-delay:1000ms]"
        />
      </div>
    </section>
  )
}
"""

        result = converter.convert(component_code)
        print("Results are:")
        print(json.dumps(result, indent=2))

        # Landing page tags example
        
        print("\n===== Landing Page Tags =====")
        tag_finder = LandingPageTagFinder()
        user_input = """
        Landing Page Goal: generate-leads
Target Audience: b2b
Product Type: digital-product
Product Name: MarketingKore
Description: MarketingKore is an AI marketing tool. That will provide landing page creation in the starting and grow it into more AI tools such as AI Forms, AI Websites, etc
        """
        # The LandingPageTagFinder now uses complete_with_json with a json_schema parameter
        # to enforce consistent output structure with categories and tags
        # tags = tag_finder.get_category_tags_map(user_input=user_input, count=5)
        # print(json.dumps(tags, indent=2))
        
        
        # JSON generator example
        # print("\n===== JSON Generator =====")
        # generator = JsonSchemaDataGenerator()
        # component_schema = {
        #   "badge": {
        #     "type": "object",
        #     "properties": {
        #       "text": {
        #         "type": "string"
        #       },
        #       "action": {
        #         "type": "object",
        #         "properties": {
        #           "text": {
        #             "type": "string"
        #           },
        #           "href": {
        #             "type": "string"
        #           }
        #         },
        #         "required": ["text", "href"],
        #         "additionalProperties": False
        #       }
        #     },
        #     "required": ["text", "action"],
        #     "additionalProperties": False
        #   },
        #   "title": {
        #     "type": "string"
        #   },
        #   "description": {
        #     "type": "string"
        #   },
        #   "actions": {
        #     "type": "array",
        #     "items": {
        #       "type": "object",
        #       "properties": {
        #         "text": {
        #           "type": "string"
        #         },
        #         "href": {
        #           "type": "string"
        #         },
        #         "icon": {
        #           "type": "object",
        #           "description": "Represents all of the things React can render.\n\nWhere {@link ReactElement} only represents JSX, `ReactNode` represents everything that can be rendered.",
        #           "additionalProperties": False
        #         },
        #         "variant": {
        #           "enum": [
        #             "default",
        #             "glow"
        #           ],
        #           "type": "string"
        #         }
        #       },
        #       "required": ["text", "href", "variant"],
        #       "additionalProperties": False
        #     }
        #   },
        #   "image": {
        #     "type": "object",
        #     "properties": {
        #       "light": {
        #         "type": "string"
        #       },
        #       "dark": {
        #         "type": "string"
        #       },
        #       "alt": {
        #         "type": "string"
        #       }
        #     },
        #     "required": ["light", "dark", "alt"],
        #     "additionalProperties": False
        #   }
        # }
        
        # # This will internally use complete_with_json with the json_schema parameter
        # data = generator.generate_data(
        #     component_schema,
        #     "Create hero section for a landing page of oneclosure.com",
        #     num_examples=1
        # )
        # print(json.dumps(data, indent=2))

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