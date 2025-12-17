# Test Agent

A simple test agent for the UiPath LangChain Python SDK.

## Description

This is a basic test agent that demonstrates the minimal structure required for a UiPath coded agent. It accepts a message as input and returns a simple response.

## Input

- `message` (string): A test message to process

## Output

- `result` (string): The processed result

## Usage

To run the agent locally, you can either:

1. Pass input directly as a JSON argument:
```bash
cd samples/test-agent
uv run uipath run agent '{"message": "Hello, World!"}'
```

2. Or use an input file:
```bash
cd samples/test-agent
echo '{"message": "Hello, World!"}' > input.json
uv run uipath run agent --input-file input.json
```

## Structure

- `graph.py`: Main agent implementation with LangGraph
- `langgraph.json`: LangGraph configuration
- `pyproject.toml`: Python project configuration and dependencies

