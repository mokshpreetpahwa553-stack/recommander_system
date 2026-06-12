import psycopg2
from fetch_youtubeVids_using_api import fetch_youtubeVideos
from difficluty_scoreANDembedding import difficulty_score,embedding

#connecting to postgres
conn = psycopg2.connect(
    host="localhost",
    database="recommander_system",
    user='postgres',
    password="Sachin1130!",
    port=5432
)

cur=conn.cursor()

'''queries = [
    "python tutorial beginner",
    "python tutorial data structures",
    "python tutorial decorators",
    "python tutorial generators",
    "python oop tutorial",
    "python projects for beginners",
    "intermediate python course",
    "advanced python course",
    "python decorators tutorial",
    "python generators tutorial",
    "python data structures tutorial",
    "python lists tuples sets dictionaries",
    "python functions tutorial",
    "python classes and objects",
    "python inheritance tutorial",
    "python polymorphism tutorial",
    "python file handling",
    "python exception handling",
    "python modules and packages",
    "python async await tutorial",
    "python metaclasses tutorial",
    "python beginner tutorial", 
    "python intermediate tutorial", 
    "python advanced tutorial",
    "python data science", 
    "python machine learning", 
    "python web development"
]'''

queries = [
    "python lambda functions tutorial",
    "python list comprehension tutorial",
    "python regex tutorial",
    "python web scraping tutorial",
    "python api fastapi tutorial",
    "python database postgresql tutorial",
    "python automation scripting",
    "python testing pytest tutorial",
    "python debugging tutorial",
    "python virtual environments tutorial",
    "python data visualization matplotlib",
    "python natural language processing nlp",
    "python computer vision opencv",
    "python neural networks deep learning",
    "python performance optimization",
    "python context managers tutorial",
    "python iterators tutorial",
    "python multithreading tutorial",
    "python design patterns tutorial",
    "python type hints tutorial",
]

k=0
for query in queries:
    videos = fetch_youtubeVideos(query)
    embed=embedding(videos).tolist() #list of each video embedding

    if len(videos[0])<8:
        continue

    all_resources_per_query=[]
    for i,v in enumerate(videos):
        row=(v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],embed[i])
        all_resources_per_query.append(row)

    cur.executemany(
        """ 
        INSERT INTO resources( title, description, resource_type, 
        difficulty_score, difficulty_category, url, source, language,embedding)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        all_resources_per_query
    )

    conn.commit()
    print(f"query {k} insertion and embedding done!")
    k+=1

print("Insertion done!")

#to remove duplicates
cur.execute(
    """
    WITH ranked AS (
    SELECT ctid,ROW_NUMBER() OVER (PARTITION BY url ORDER BY display_id) AS rn FROM resources)
    DELETE FROM resources
    WHERE ctid IN (
    SELECT ctid
    FROM ranked
    WHERE rn > 1
    )
    """
)
conn.commit()
print("Duplicates removed!!")

cur.close()
conn.close()

difficulty_score()


print("DONE!!")

