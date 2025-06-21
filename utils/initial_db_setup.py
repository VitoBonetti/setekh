from queries.initial_setup import queries


def execute_query(conn):
    cursor = conn.cursor()
    for query in queries:
        try:
            cursor.execute(query)
            conn.commit()
            print('Query executed successfully')
        except Exception as e:
            print(e)
    cursor.close()
    conn.close()