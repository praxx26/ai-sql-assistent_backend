import mysql.connector


def get_history_connection():

    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Praga08@@",
        database="ai_sql_history"
    )

    return conn