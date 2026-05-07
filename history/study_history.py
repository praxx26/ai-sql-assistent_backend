from database.history_connection import get_history_connection


def save_study_history(question, sql_query, explanation):
    conn = get_history_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO study_history
    (question, sql_query, explanation)
    VALUES (%s, %s, %s)
    """
    values = (
        question,
        sql_query,
        explanation
    )
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

def get_study_history():
    conn = get_history_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT * FROM study_history
    ORDER BY created_at DESC
    """)
    history = cursor.fetchall()
    cursor.close()
    conn.close()

    return history


def delete_study_history():
    conn = get_history_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM study_history")
    conn.commit()
    cursor.close()
    conn.close()