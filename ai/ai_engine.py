from openai import OpenAI as ai
import os
from dotenv import load_dotenv
import sqlparse

load_dotenv()

client=ai(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def generate_sql(schema, question):
    prompt = f"""
    You are an expert SQL generator.

    Use ONLY the tables and columns provided.

    Database Schema:
    {schema}

    User Question:
    {question}

    Rules:
- Generate only SQL
- Generate ONLY MySQL compatible SQL
- Use valid MySQL syntax
- Use LIMIT instead of TOP
- Do not use SQL Server syntax
- Do not use PostgreSQL specific syntax
- No explanation
- No markdown
- Use ONLY provided tables and columns
- Do not hallucinate columns
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=0
    )

    sql_query = response.choices[0].message.content.strip()
    sql_query = sql_query.replace("```sql", "").replace("```", "")
    formatted_sql = sqlparse.format(
        sql_query,
        reindent=True,
        keyword_case='upper'
    )

    return formatted_sql
    
def generate_study_sql(question):
    prompt=f"""
    You are an expert SQL generator.

    convert the natural language into SQL query.
Rules:
- Generate only SQL
- Generate ONLY MySQL compatible SQL
- Use valid MySQL syntax
- Use LIMIT instead of TOP
- Do not use SQL Server syntax
- Do not use PostgreSQL specific syntax
- No explanation
- No markdown
- Use ONLY provided tables and columns
- Do not hallucinate columns

    User Question:
    {question}

    SQL:
    """

    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    sql_query = response.choices[0].message.content.strip()
    sql_query = sql_query.replace("```sql", "").replace("```", "")
    formatted_sql = sqlparse.format(
        sql_query,
        reindent=True,
        keyword_case='upper'
    )
    return formatted_sql