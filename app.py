import os
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    recap = request.json["recap"]

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system="""
        You are an energetic NBA analyst. Summarize game recaps in a fun, engaging, and informative way.
        Use plain text only, no markdown formatting.
        """,
        messages=[
            {"role": "user", "content": f"Summarize the following NBA game recap: {recap}"}
        ]
    )

    return jsonify({"summary": response.content[0].text})

if __name__ == "__main__":
    app.run(debug=True)