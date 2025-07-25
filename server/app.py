from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import requests

app = Flask(__name__)
CORS(app)

TOGETHER_API_KEY = "97f2e2e43d184a56e60f1895332ede2ccdb9e7fb7260d7c74fe2c74989c17d3a"
#os.getenv("TOGETHER_API_KEY")  # Or hardcode it if needed
MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    url = data.get("url")

    try:
        result = subprocess.run(["python", "./scraper/scrape.py", url], capture_output=True, text=True)
        website_text = result.stdout
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    prompt = f"""Analyze the following website content and suggest 5–7 blog post ideas:\n\n{website_text}"""

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return jsonify({"blog_ideas": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
