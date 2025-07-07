"""Setup script for the LLM completion library."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="llm-completion",
    version="0.1.0",
    author="innerkoreDev",
    author_email="example@example.com",
    description="A library for LLM text completion using LiteLLM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/llm-completion",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "litellm>=1.0.0",
        "tenacity>=8.2.0",  # Updated version
        "python-dotenv>=0.19.0",
        "jsonschema>=4.0.0",  # Added for schema validation
    ],
)