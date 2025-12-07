# ARKOS

ARK (Automated Resource Knowledgebase) revolutionizes resource management via automation. Using advanced algorithms, it streamlines collection, organization, and access to resource data, facilitating efficient decision-making.


## Languages and Dependencies

The entire codebase is in Python, except for a few shell scripts. 

### Core Dependencies

* **`openai>=1.61.0`** - OpenAI Python SDK for standardizing inference engine communication and API compatibility
* **`pyyaml>=6.0.2`** - YAML parser for configuration files (state graphs, etc.)
* **`pydantic>=2.10.6`** - Data validation and schema definition using Python type annotations
* **`requests>=2.32.3`** - HTTP library for making API requests to external services and tools

### Web Framework

* **`fastapi>=0.115.0`** - Modern, fast web framework for building the API server with automatic OpenAPI documentation
* **`uvicorn>=0.32.0`** - ASGI server for running FastAPI applications

### Database & Memory

* **`psycopg2-binary>=2.9.11`** - PostgreSQL adapter for Python (binary distribution, no compilation required). Used for storing conversation context and long-term memory
* **`mem0ai`** - Memory management library for vector-based memory storage and retrieval using Supabase

### Installation

Install all dependencies using:

```bash
pip install -r requirements.txt
```

**Note:** `psycopg2-binary` is used instead of `psycopg2` to avoid requiring PostgreSQL development libraries (`libpq-dev`) on the system. For production deployments, you may want to use `psycopg2` with proper system dependencies.

## File structure

(As of September 11, 2025.)


* `base_module/` for main interface
* `config_module/` for YAML configuration files
* `model_module/` for core LLM-inference logic
* `agent_module/` for agentic structure 
* `state_module/` for defining agent state graphs 
* `tool_module/` for MCP compatibility 
* `memory_module/` for long term memory and context management
* `schemas/` for JSON schemas when communicating between frontend and backend
* `state_module/`
* `tool_module/`
* `.gitignore`
* `README.md` (this very file)
* `requirements.txt` (Python dependencies)

## Instructions

### Start Inference Engine

The project uses SGLang to run the Qwen 2.5-7B-Instruct model. Start the inference server:

```bash
bash model_module/run.sh
```

This will start the SGLang server on port 30000. The model Qwen/Qwen2.5-7B-Instruct is currently in use.

### Running the Application

You need to run both the API server and the test interface:

1. **Start the API server** (in one terminal):
   ```bash
   cd base_module
   python app.py
   ```
   This starts the FastAPI server on port 1111, providing the `/v1/chat/completions` endpoint.

2. **Run the test interface** (in another terminal):
   ```bash
   cd base_module
   python main_interface.py
   ```
   This provides an interactive CLI to test the agent. Type your messages and press Enter. Type `exit` or `quit` to stop.

## Contributors + contact

| Name                  | Role           | GitHub username | Affiliation   |
| --------------------  | -------------- | --------------- | --------------|
| Nathaniel Morgan      | Project leader | nmorgan         | MIT           |
| Joshua Guo            | Frontend       | duck_master     | MIT           |
| Ilya Gulko            | Backend        | gulkily         | MIT           |
| Jack Luo              | Backend        | thejackluo      | Georgia Tech  |
| Bryce Roberts         | Backend        | BryceRoberts13  | MIT           |
| Angela Liu            | Backend        | angelaliu6      | MIT           |
| Ishaana Misra         | Backend        | ishaanam        | MIT           |
