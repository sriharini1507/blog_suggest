import subprocess
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from scraper.scrape import extract_text_from_url
from dotenv import load_dotenv

load_dotenv()  # load from .env file

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = Flask(__name__)
CORS(app)

groq_client = Groq(api_key=GROQ_API_KEY)
MODEL = "llama3-70b-8192"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    url = data.get("url")

    try:
        website_text = extract_text_from_url(url)

        # Improved check: skip if Playwright error content shows up
        if not website_text.strip() or "ERR_HTTP2_PROTOCOL_ERROR" in website_text:
            return jsonify({
                "error": "Could not extract meaningful website content. Try a different site."
            }), 400

    except Exception as e:
        return jsonify({"error": f"Scraper error: {str(e)}"}), 500

    try:
        response = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI content strategist. Your task is to output ONLY 5 to 7 blog post title suggestions based on the user's input. "
                        "Do not add any introduction, assumptions, or explanations. "
                        "Return each title on a new line with no numbering, quotes, or bullet points. "
                        "The output should ONLY be plain blog titles directly relevant to the provided content."
                    )
                },
                {
                    "role": "user",
                    "content": website_text
                }
            ],
            model=MODEL,
            temperature=0.7,
            max_tokens=512
        )

        print("✅ Returning blog ideas")
        return jsonify({"blog_ideas": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": f"Groq API error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
