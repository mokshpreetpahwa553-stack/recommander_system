import psycopg2
import os
from dotenv import load_dotenv

def extraction(resource_type):
    
    load_dotenv()
    DATABASE_PASS = os.getenv("DATABASE_PASSWORD")

    #connecting to postgres
    conn = psycopg2.connect(
        host="localhost",
        database="recommander_system",
        user='postgres',
        password=DATABASE_PASS,
        port=5432
    )

    cur=conn.cursor()

    if resource_type=='videos':
        cur.execute(
            '''
            SELECT title,description,difficulty_score,difficulty_category,resource_type,url,source,language,embedding FROM resources WHERE resource_type='video' ''',
        )
    elif resource_type=='article':
        cur.execute(
                '''
                SELECT title,description,difficulty_score,difficulty_category,resource_type,url,source,language,embedding FROM resources WHERE resource_type='article' ''',
        )

    rows=cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()

    return rows

def fetch_resources(resource_type):
    rows = extraction(resource_type)
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
            
