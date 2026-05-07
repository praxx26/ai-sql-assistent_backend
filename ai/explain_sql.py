from openai import OpenAI as ai
from dotenv import load_dotenv 
import os

load_dotenv()

client = ai(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def explain_sql(sql_query):
    prompt= f"""
    You are an SQL expert.

    Explain the following SQL query in simple English.

    SQL Query:
    {sql_query}

    Rules:
    -if they provide with DB give the exlanation in 3 to 4 lines 
    - if the user does not provide db give me the clear eplanation about each line and each word why we used like that 
    - Keep it concise
    - Beginner friendly
    - Focus only on what the query does
    - Keep explanation beginner friendly
    - Do not generate SQL
    """

    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    explanation = response.choices[0].message.content.strip()

    return explanation