# LLM Generate Function

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![GitHub Issues](https://img.shields.io/github/issues/simonpierreboucher/llm-generate-function)](https://github.com/simonpierreboucher/llm-generate-function/issues)
[![GitHub Forks](https://img.shields.io/github/forks/simonpierreboucher/llm-generate-function)](https://github.com/simonpierreboucher/llm-generate-function/network)
[![GitHub Stars](https://img.shields.io/github/stars/simonpierreboucher/llm-generate-function)](https://github.com/simonpierreboucher/llm-generate-function/stargazers)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Models Supported](#models-supported)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Using the Python Module](#using-the-python-module)
  - [Running the Jupyter Notebook](#running-the-jupyter-notebook)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

In the rapidly evolving field of artificial intelligence, Language Learning Models (LLMs) play a crucial role in various applications, from natural language understanding to content generation. This repository provides a **modular and extensible framework** to generate and compare responses from a diverse set of LLMs provided by **OpenAI**, **Anthropic**, and **Mistral**.

By leveraging a unified Python function, users can seamlessly interact with multiple LLM providers, facilitating benchmarking, comparison, and integration into larger projects. The accompanying Jupyter Notebook serves as a practical example to demonstrate the functionality and versatility of the provided tools.

## Features

- **Multi-Provider Support**: Interact with OpenAI, Anthropic, and Mistral models using a single function.
- **Flexible Configuration**: Customize parameters such as temperature, max tokens, and top_p for tailored responses.
- **Markdown Formatting**: Responses are formatted in Markdown for easy readability within Jupyter Notebooks.
- **Secure API Key Management**: Utilize environment variables to manage API keys securely.
- **Extensible Design**: Easily add support for additional LLM providers or models as needed.
- **Comprehensive Documentation**: Detailed instructions and examples to get you started quickly.

## Models Supported

### **OpenAI**
- `gpt-4o`
- `gpt-4o-mini`
- `gpt-4-turbo`
- `gpt-4`
- `gpt-3.5-turbo`

### **Anthropic**
- `claude-3-5-sonnet-20241022`
- `claude-3-opus-20240229`
- `claude-3-sonnet-20240229`
- `claude-3-haiku-20240307`

### **Mistral**
- `mistral-small-latest`
- `mistral-medium-latest`
- `mistral-large-latest`
- `open-mistral-7b`
- `open-mixtral-8x7b`
- `open-mixtral-8x22b`

## Installation

### Prerequisites

- **Python 3.7 or higher**: Ensure you have Python installed. You can download it from [here](https://www.python.org/downloads/).

### Clone the Repository

```bash
git clone https://github.com/simonpierreboucher/llm-generate-function.git
cd llm-generate-function
```

### Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv env
# Activate the virtual environment
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### Setting Up API Keys

The project requires API keys from OpenAI, Anthropic, and Mistral to interact with their respective models. These keys should be stored securely in a `.env` file.

1. **Create a `.env` File**

   In the root directory of the project, create a file named `.env`:

   ```bash
   touch .env
   ```

2. **Add Your API Keys**

   Open the `.env` file in a text editor and add your API keys in the following format:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```

   **Important**: Ensure that the `.env` file is **never** committed to version control. The provided `.gitignore` already excludes it, but double-check to prevent accidental exposure.

## Usage

### Using the Python Module

You can utilize the `generate_and_format_response` function in your Python scripts or other modules.

```python
import os
from IPython.display import display, Markdown
from llm_utils import generate_and_format_response

# Define conversation messages
messages = [
    {"role": "user", "content": "Explain the concept of quantum entanglement and how it challenges classical notions of locality and realism."}
]

# Generate and format the response from OpenAI
formatted_response_openai = generate_and_format_response(
    provider="openai",                    # Change to "anthropic" or "mistral" if necessary
    model="gpt-4o-mini",                  # Adjust the model for the chosen provider
    messages=messages,
    temperature=0.7,
    max_tokens=1500,
    top_p=0.9
)

# Display the formatted response
display(Markdown(formatted_response_openai))
```

### Running the Jupyter Notebook

An example Jupyter Notebook (`example.ipynb`) is provided to demonstrate how to use the module with all supported models.

1. **Launch Jupyter Notebook**

   ```bash
   jupyter notebook
   ```

2. **Open `example.ipynb`**

   Navigate to the `example.ipynb` file in the Jupyter interface and run the cells to generate and view responses from each model.

## Examples

Below is an example of how to use the `generate_and_format_response` function with multiple models.

```python
import os
from IPython.display import display, Markdown
from llm_utils import generate_and_format_response

# Define the list of models grouped by provider
providers_models = {
    "mistral": [
        "mistral-small-latest",
        "mistral-medium-latest",
        "mistral-large-latest",
        "open-mistral-7b",
        "open-mixtral-8x7b",
        "open-mixtral-8x22b"
    ],
    "anthropic": [
        "claude-3-5-sonnet-20241022",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307"
    ],
    "openai": [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-4",
        "gpt-3.5-turbo"
    ]
}

# Define the base conversation message
base_message = {
    "role": "user",
    "content": "Explain the concept of quantum entanglement and how it challenges classical notions of locality and realism."
}

# Additional message for Mistral models to provide a more detailed prompt
additional_mistral_message = " What are the implications of entanglement for our understanding of causality and information transfer?"

# Iterate over each provider and their models
for provider, models in providers_models.items():
    for model in models:
        # Define messages based on the provider
        if provider == "mistral":
            messages = [
                {
                    "role": "user",
                    "content": base_message["content"] + additional_mistral_message
                }
            ]
        else:
            messages = [base_message]
        
        # Determine max_tokens based on provider (adjust as needed)
        max_tokens = 2000 if provider == "mistral" else 1500
        
        # Generate and format the response
        formatted_response = generate_and_format_response(
            provider=provider,
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=max_tokens,
            top_p=0.9
        )
        
        # Display the response with provider and model information
        display(Markdown(f"### Provider: **{provider.capitalize()}** | Model: **{model}**"))
        display(Markdown(formatted_response))
        display(Markdown("---"))  # Separator for readability
```

## Contributing

Contributions are welcome! Whether you're reporting a bug, suggesting a feature, or improving the documentation, your input is valuable.

### Steps to Contribute

1. **Fork the Repository**

   Click the "Fork" button at the top right of the repository page to create your own fork.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/your_username/llm-generate-function.git
   cd llm-generate-function
   ```

3. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

4. **Make Your Changes**

   Implement your feature, fix bugs, or update documentation.

5. **Commit Your Changes**

   ```bash
   git add .
   git commit -m "Add detailed explanation for quantum entanglement"
   ```

6. **Push to Your Fork**

   ```bash
   git push origin feature/YourFeatureName
   ```

7. **Create a Pull Request**

   Navigate to the original repository and click "Compare & pull request". Provide a clear description of your changes.

### Code of Conduct

Please adhere to the [Code of Conduct](CODE_OF_CONDUCT.md) in all interactions within the project.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions, suggestions, or feedback, please open an issue on [GitHub Issues](https://github.com/simonpierreboucher/llm-generate-function/issues) or contact [Simon Pierre Boucher](mailto:simon.pierre.boucher@example.com).

