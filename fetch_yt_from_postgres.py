import psycopg2

def extraction():
    conn=psycopg2.connect(
        host="localhost",
        database="recommander_system",
        user="postgres",
        password="Sachin1130!",
        port = 5432
    )

    cur=conn.cursor()

    cur.execute(
        '''
        SELECT title,description,difficulty_score,difficulty_category,resource_type,url,source,language,embedding FROM resources''',
    )
    rows=cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()

    return rows

def fetch_resources():
    rows = extraction()
    resources=[]

    for row in rows:

        resources.append({
            "title": row[0],
            "description": row[1],
            "difficulty_score": row[2],
            "difficulty_category": row[3],
            "format": row[4],
            "url": row[5],
            "source": row[6],
            "language": row[7],
            "embedding": row[8],
            "score": 0
        })

    return resources
            
