from database.history_connection import get_history_connection
import json


def save_execute_history(
    database_name,
    question,
    sql_query,
    explanation,
    results
    ):
    conn = get_history_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO execute_history
    (database_name, question, sql_query, explanation, results)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        database_name,
        question,
        sql_query,
        explanation,
        json.dumps(results)
    )
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()


def get_execute_history():
    conn = get_history_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT * FROM execute_history
    ORDER BY created_at DESC
    """)
    history = cursor.fetchall()
    cursor.close()
    conn.close()
    return history


def delete_execute_history():
    conn = get_history_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM execute_history")
    conn.commit()
    cursor.close()
    conn.close()