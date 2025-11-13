import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
# Direct API key
openai.api_key = "YOUR_OPENAPI_KEY"

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello"}],
        temperature=0
    )
    print("✅ API works!")
    print("Response:", response['choices'][0]['message']['content'])
except Exception as e:
    print(f"❌ API Error: {e}")