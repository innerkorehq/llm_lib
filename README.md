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

# Initialize the tag finder
tag_finder = LandingPageTagFinder()

# Find tags
components = ["Hero", "Features", "Pricing", "Testimonials", "FAQ", "CTA", "Footer"]
tags = tag_finder.find_tags(components, count=5)
print(tags)
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