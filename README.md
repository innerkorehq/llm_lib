# LLM Completion Library

A Python library for LLM text completion using LiteLLM with Gemini flash 2.5 and OpenAI fallback support.

## Features

- General interface for text completion with multiple LLM providers
- Primary support for Google's Gemini flash 2.5 model
- Automatic fallback to OpenAI when needed
- Comprehensive error handling and logging
- Specialized implementations for common tasks:
  - Converting Shadcn components to TypeScript
  - Finding tags for landing pages
  - Generating JSON data based on schemas
- Built-in landing page tagging system with CLI tools

## Installation

```bash
pip install llm-completion
```

## Configuration

Set the following environment variables:

```bash
# Primary provider (Gemini)
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=models/gemini-flash-2.5  # Default value

# Fallback provider (OpenAI)
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o  # Default value

# Optional settings
GEMINI_MAX_RETRIES=3  # Default value
GEMINI_TIMEOUT=30     # Default value in seconds
OPENAI_MAX_RETRIES=3  # Default value
OPENAI_TIMEOUT=30     # Default value in seconds
MAX_TOKENS=4096       # Default value
TEMPERATURE=0.7       # Default value
```

## Basic Usage

```python
from llm_completion import LiteLLMCompletion

# Initialize the completion provider
completion = LiteLLMCompletion()

# Generate a text completion
result = completion.complete("Tell me about the solar system")
print(result)

# Generate a JSON completion
json_result = completion.complete_with_json(
    "List the planets in the solar system with their key characteristics"
)
print(json_result)

# Generate a JSON completion with schema validation
schema = {
    "type": "object",
    "properties": {
        "planets": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string"},
                    "diameter": {"type": "number"},
                    "hasRings": {"type": "boolean"}
                },
                "required": ["name", "type"]
            }
        }
    }
}

json_result_with_schema = completion.complete_with_json(
    "List the planets in the solar system with their key characteristics",
    json_schema=schema
)
print(json_result_with_schema)
```

## Specialized Implementations

### Converting Shadcn Components to TypeScript

```python
from llm_completion.implementations import ShadcnToTypeScriptConverter

# Initialize the converter
converter = ShadcnToTypeScriptConverter()

# Convert a component
component_code = """
function Button({ children }) {
  return <button className="px-4 py-2 bg-blue-500 text-white">{children}</button>
}
"""

ts_component, props_file, metadata = converter.convert(component_code)
print(ts_component)
print(props_file)
print(metadata)
```

### Finding Landing Page Tags

```python
from llm_completion.implementations import LandingPageTagFinder

# Initialize the tag finder (use built-in tag data, no API calls needed)
tag_finder = LandingPageTagFinder(use_api=False)

# Find tags
components = ["Hero", "Features", "Pricing", "Testimonials", "FAQ", "CTA", "Footer"]
tags = tag_finder.get_category_tags_map(components, count=5)
print(tags)

# Get recommended tags for a specific component
hero_tags = tag_finder.get_tags_for_component("Hero")
print(hero_tags)
```

### Generating JSON Data

```python
from llm_completion.implementations import JsonSchemaDataGenerator

# Initialize the generator
generator = JsonSchemaDataGenerator()

# Define a schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 18, "maximum": 100},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["name", "email"]
}

# Generate data
data = generator.generate_data(
    schema,
    "Create profiles for tech industry professionals",
    num_examples=3
)
print(data)
```

## Tag Management System

The library includes a comprehensive tag management system for landing page components, with no need for API calls:

```python
from llm_completion.tag_manager import TagManager

# Initialize the tag manager
tag_manager = TagManager()

# Search for tags
mobile_tags = tag_manager.search_tags("mobile")
print(mobile_tags)

# Get recommended component combinations
components = tag_manager.get_component_combinations(count=5, focus="conversion")
print(components)

# Create a balanced set of tags for a component
tags = tag_manager.create_tag_set("hero", additional_count=3)
print(tags)
```

## Command Line Interface

The library provides a command-line interface for tag management:

```bash
# Search for tags
python -m llm_completion tags search mobile

# List recommended components
python -m llm_completion tags list --count=5 --focus=conversion

# Get tags for a component
python -m llm_completion tags tags Hero

# Export tag data
python -m llm_completion tags export --format=json --output=tags.json

# Analyze landing page components
python -m llm_completion tags analyze --components=components.json
```

## Error Handling

The library provides specific exceptions for different error scenarios:

```python
from llm_completion import (
    CompletionError,
    APIKeyError,
    RateLimitError,
    ModelNotAvailableError,
    InvalidRequestError,
    LLMTimeoutError,
)

try:
    result = completion.complete("My prompt")
except RateLimitError:
    print("Rate limit exceeded, try again later")
except APIKeyError:
    print("API key issue, check your configuration")
except LLMTimeoutError:
    print("Request timed out, try again later")
except CompletionError as e:
    print(f"Error during completion: {str(e)}")
```

## License

MIT