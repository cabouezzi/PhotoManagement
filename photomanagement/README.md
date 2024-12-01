# Package for Photomanagement
## Dependencies
### Ollama
Follow instructions to download and run Ollama at https://ollama.com/download and pull the vision LLM being used with `ollama pull llama3.2-vision:11b`.

Ollama is used to host a server for communicating with LLM's, which is more memory efficient than simply loading models into memory.

## Development
**Highly recommended** to work in an isolated environment, using the [Poetry](https://python-poetry.org) dependency manager and packaging tool.
```bash
      $ python3.9 -m venv env
      $ source env/bin/activate
(env) $ pip install poetry
```

### pyttsx3
Requires python3 version at least 3.6.3
Install the module: 
```pip install pyttsx3```