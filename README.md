# ECE498-Final-Project

## How to Run the Backend Server

### 1. Activate the Conda Environment

```bash
conda activate rag
cd ECE498-FP/server
```

### 2. Add Your OpenAI API Key

In `ECE498-FP/server/embedding.py`, replace the `api_key` value with your own OpenAI API key:

```python
openai_client = OpenAI(api_key="enter_your_api_key_here")
```

### 3. Start the FastAPI Server

```bash
python main.py
```

---
