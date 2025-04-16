# Generative AI

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install tiktoken

# Freeze the environment
pip freeze > requirements.txt

# Install from requirements.txt
pip install -r requirements.txt

# Install OpenAI
pip install openai

# Install Python Environment
pip install python-dotenv

# Install Google Gemini
pip install google-genai

# Start Docker Compose
docker compose up

# Pull Ollama Image to Fast API Server
python ollama_api.py

# Install uvicorn
pip install uvicorn

# Start FastAPI Server
uvicorn ollama_api:app --port 8000
```
