import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

class LLM:

    def __init__(self):
        load_dotenv(Path(__file__).resolve().parents[2] / ".env")

        self.gemini = ChatGoogleGenerativeAI(
            model="gemini-3.8-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0
        )

        self.groq = ChatGroq(
            model="openai/gpt-oss-20b",
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0
        )

    def generate(self, prompt: str) -> str:

        # Try Gemini first
        try:
            response = self.gemini.invoke(prompt)

            if response.content:
                print("Generated using Gemini")
                return response.content

        except Exception as e:
            print(f"Gemini failed: {e}")
            print("Falling back to Groq...")

        # Try Groq
        try:
            response = self.groq.invoke(prompt)

            if response.content:
                print("Generated using Groq")
                return response.content

        except Exception as e:
            print(f"Groq failed: {e}")

        return (
            "I'm sorry, but I couldn't generate an answer "
            "right now. Please try again later."
        )