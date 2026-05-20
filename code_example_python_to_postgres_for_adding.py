import psycopg2

#connecting to postgres
conn = psycopg2.connect(
    host="localhost",
    database="recommander_system",
    user='postgres',
    password="Sachin1130!",
    port=5432
)

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
