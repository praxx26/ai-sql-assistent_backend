from openai import OpenAI as ai
from dotenv import load_dotenv
import os

load_dotenv()

client = ai(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def explain_sql(sql_query, mode="database"):

    if mode == "study":

        prompt = f"""
        You are an expert SQL teacher.

        Explain the following SQL query in a detailed beginner-friendly way.

        SQL Query:
        {sql_query}

        Rules:
- Explain ONLY the SQL clauses present in the query
- Do not explain unnecessary SQL keywords
- Explain the query line by line
- Explain each keyword separately only if it exists in the query
- For each line explain:
  - what it does
  - why it is used
  - what output it affects
- Use simple beginner-friendly English
- Keep explanations clean and structured
- Use numbered points
- Put each point on a new line
- Explain symbols like * only if present
- Explain WHERE, GROUP BY, ORDER BY, JOIN, LIMIT only if present
- Do not explain concepts not used in the query
- Keep explanation practical and concise
- Add a short final summary of what the query does
- Do not generate SQL
- Do not use markdown
        """

    else:

        prompt = f"""
        You are an SQL expert.

        Explain the following SQL query briefly.

        SQL Query:
        {sql_query}

        Rules:
        - Keep explanation concise
        - Keep it between 3 to 5 lines
        - Beginner friendly
        - Focus only on what the query does
        - Do not generate SQL
        """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    explanation = response.choices[0].message.content.strip()

    return explanation