def get_schema(conn):

    cursor = conn.cursor()

    query = """
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
    ORDER BY table_name;
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    schema = ""

    current_table = None

    for table, column in rows:

        if table != current_table:

            schema += f"\nTable: {table}\nColumns: "

            current_table = table

        schema += f"{column}, "

    return schema