import requests

URL = "http://localhost:11434/api/generate"

def ask_ai(question):

    prompt = f"""
You are a smart assistant for blind people.

Rules:
- Answer in simple Arabic.
- Keep answers short.
- Be friendly.
- If there is danger, warn the user clearly.

User question: {question}
"""

    data = {
        "model": "tinyllama",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(URL, json=data)
        result = response.json()
        return result["response"]

    except:
        return "حدث خطأ في النظام"