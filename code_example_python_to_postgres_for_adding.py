from db_config import get_connection

#connecting to postgres
conn = get_connection()

#creating cursor
cur=conn.cursor()

#inserting data
cur.executemany(
    """
    INSERT INTO resource_types (name)
    VALUES (%s)
    """,
    [("videos",),("articles",)]
)

#commiting command
conn.commit()

#closing
cur.close()
conn.close()

print("DONE!!")
