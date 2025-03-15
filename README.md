# Lacework Agent with Vector Store

A Python-based tool for creating and managing a vector store of Lacework CLI documentation, enabling semantic search and question answering capabilities.

## Overview

This tool allows you to:

1. Create a vector store using OpenAI's API
2. Upload Lacework CLI documentation to the vector store
3. Query the vector store with natural language questions
4. Verify and manage the vector store contents

By leveraging OpenAI's vector store capabilities, this tool enables you to quickly find information about Lacework CLI commands and functionality without having to manually search through documentation.

## Prerequisites

- Python 3.8+
- OpenAI API key
- Lacework CLI documentation files (markdown format)

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Creating and Updating the Vector Store

To create a new vector store or update an existing one with all Lacework CLI documentation:

```bash
python3 lacework_agent.py --update
```

### Adding Specific Files to the Vector Store

To add only files that start with "lacework" to the vector store:

```bash
python3 lacework_agent.py --attach_files
```

### Verifying the Vector Store

To check the status of files in the vector store:

```bash
python3 lacework_agent.py --verify
```

For a simpler verification output:

```bash
python3 lacework_agent.py --simple-verify
```

### Asking Questions

To query the vector store with natural language questions:

```bash
python3 lacework_agent.py --prompt "What is the Lacework CLI and what can I do with it?"
```

Example questions:
- "How do I list Lacework agents using the CLI?"
- "What commands are available for managing alert channels?"
- "How can I configure Lacework CLI profiles?"

### Using the Agent for Complex Tasks

The agent can solve more complex tasks and return bash commands using two different approaches:

#### Using the Direct OpenAI API (Default)

```bash
python3 lacework_agent.py --agent "Set up monitoring for a new AWS account"
```

This approach:
1. Searches the vector store for relevant information
2. Generates a series of bash commands to accomplish the task
3. Outputs the commands with explanatory comments
4. Saves a detailed trace of the execution process locally

#### Using the OpenAI Agents SDK with Vector Search

```bash
python3 lacework_agent.py --agentsdk "Set up monitoring for a new AWS account"
```

This approach:
1. Uses the OpenAI Agents SDK to run the agent
2. First searches the vector store for relevant documentation
3. Provides the documentation context to the agent
4. Generates bash commands based on the documentation
5. May send traces to OpenAI by default (as per the SDK's behavior)

Note: To use the `--agentsdk` parameter, you need to install the OpenAI Agents SDK:
```bash
pip install openai-agents
```

Example tasks for either approach:
- "Configure alert channels for Slack and email"
- "Set up compliance reporting for AWS accounts"
- "Create a new resource group and add resources to it"

### Tracing

The agent automatically records detailed traces of each run, which are saved **locally** in the `traces/` directory. These traces are **not** sent to OpenAI or any external service - they remain on your system for your reference only. Each trace includes:

- Task description
- Timestamps for each step
- Inputs and outputs for each step
- Models and tools used
- Final output or error information

Traces are saved as JSON files with the format `agent_run_YYYYMMDD_HHMMSS.json`. These traces are useful for:

- Debugging agent behavior
- Analyzing performance
- Understanding the agent's reasoning process
- Auditing the agent's actions
- Maintaining a history of agent operations for compliance purposes

Since traces contain the full context of your interactions, including prompts and responses, they provide complete transparency while maintaining privacy.

### Retrying Failed Files

If some files failed to upload, you can retry them:

```bash
python3 lacework_agent.py --retry-failed
```

### Deleting the Vector Store

To delete the vector store and clean up associated files:

```bash
python3 lacework_agent.py --delete
```

## Configuration

The tool uses a configuration file (`lacework_vector_store_config.json`) to store the vector store ID. This file is created automatically when you first run the tool.

## Directory Structure

- `lacework_cli_docs/`: Directory containing Lacework CLI documentation files
- `logs/`: Directory containing log files
- `lacework_vector_store_config.json`: Configuration file storing the vector store ID

## Logging

Logs are stored in the `logs/` directory with timestamps. Each run of the tool creates a new log file with the format `lacework_agent_YYYYMMDD_HHMMSS.log`.

## Troubleshooting

### API Key Issues

If you encounter errors related to the OpenAI API key:
1. Ensure your API key is correctly set in the `.env` file
2. Check that the `.env` file is in the correct location
3. Verify that your OpenAI account has access to the vector store API

### File Upload Issues

If files fail to upload to the vector store:
1. Run `python3 lacework_agent.py --verify` to identify failed files
2. Use `python3 lacework_agent.py --retry-failed` to retry uploading failed files
3. Check the logs for specific error messages

### Rate Limiting

If you encounter rate limiting issues:
1. Use the `--attach_files` option to upload files one by one
2. Add delays between operations by modifying the code
3. Consider upgrading your OpenAI API plan

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.