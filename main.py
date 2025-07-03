from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
from dotenv import load_dotenv
import os

# Setup OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route("/", methods=["POST"])
def bot():
    user_msg = request.values.get('Body', '').strip()
    response = MessagingResponse()

    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful WhatsApp assistant."},
                {"role": "user", "content": user_msg}
            ]
        )
        answer = chat_completion.choices[0].message.content.strip()
        response.message(answer)

    except Exception as e:
        response.message("Sorry, error from ChatGPT:\n" + str(e))

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
