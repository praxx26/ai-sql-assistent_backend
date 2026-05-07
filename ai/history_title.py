from openai import OpenAI as ai
from dotenv import load_dotenv
import os

load_dotenv()

client=ai(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def generate_history_title(question):

    prompt = f"""
    Convert the following user request into a short professional title.

    User Request:
    {question}

    Rules:
    - Maximum 5 words
    - Professional
    - Clear
    - No punctuation
    - Return only title
    """

    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()