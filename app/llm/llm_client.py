import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

        if not self.api_key:
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key)

    def generate(self, messages: list[dict] | str) -> str:
        if not self.client:
            return "LLM API key is missing. Please configure GROQ_API_KEY."

        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
            max_tokens=700
        )

        return response.choices[0].message.content.strip()