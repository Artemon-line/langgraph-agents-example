# langgraph-rag-agent-example

🚀 This repository contains hands-on examples from [LangGraph Complete Course for Beginners – Complex AI Agents with Python by Vaibhav Mehra](https://www.youtube.com/watch?v=jGg_1h0qzaM).

🦙 **LLAMA Models Used:**  
Instead of OpenAI, this repo uses `llama3.2:latest` and `nomic-embed-text` models via Ollama.  
Make sure your Ollama server is running and both models are downloaded before running the code:

```sh
ollama pull llama3.2:latest
ollama pull nomic-embed-text
```

🧪 **Notebook Testing:**  
This repository also demonstrates how to use Jupyter notebooks as test cases, following the approach from [Jupyter Notebook Testing](https://blog.iqmo.com/blog/python/jupyter_notebook_testing/).
Test results are formatted using pytest-json-crtf for better readability and CI/CD integration.

Key features:

- Automated notebook execution validation
- Dynamic test generation for notebooks
- Detailed test reporting with JSON output
- GitHub Actions integration
- Coverage reporting for notebook code

To run notebook tests:

```sh
pytest tests/nb_tests/test_nb.py --ctrf test-reports/ctrf/nb-tests.report.json
```

💡 Explore how to build complex AI agents with Python, LangGraph, and LangChain!
