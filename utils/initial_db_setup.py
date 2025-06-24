from queries.queries import INITIAL_QUERIES


def execute_query(conn):
    cursor = conn.cursor()
    for query in INITIAL_QUERIES:
        try:
            cursor.execute(query)
            conn.commit()
            print('Query executed successfully')
        except Exception as e:
            print(e)
    # cursor.close()
    # conn.close()