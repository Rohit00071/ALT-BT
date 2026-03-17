from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL_NAME")

print(f"Testing Groq with model: {model}")
client = Groq(api_key=api_key)

try:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say hello",
            }
        ],
        model=model,
    )
    print("Response:", chat_completion.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
