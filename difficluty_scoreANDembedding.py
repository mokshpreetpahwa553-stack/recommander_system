import psycopg2
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer

#fetching all resources
conn=psycopg2.connect(
    host="localhost",
    database="recommander_system",
    user="postgres",
    password="Sachin1130!",
    port = 5432
)

cur=conn.cursor()

cur.execute(
    """
    SELECT id,title,description FROM resources
    """
)
full_text=[]
ids=[]
rows=cur.fetchall()

for row in rows:
    full_text.append((row[1]+' ' + row[2]).lower())
    ids.append(row[0])


model = joblib.load('text_scorer_pipeline.pkl')
scores = model.predict(full_text)

#normalising scores
scores = (scores-scores.mean())/scores.std()

low_cut = np.percentile(scores, 33)
high_cut = np.percentile(scores, 67)

#now enbeddings of each row
model=SentenceTransformer("all-MiniLM-L6-v2")
embed = model.encode(full_text,normalize_embeddings=True)

updates=[]
for i in range(len(ids)):
    diff_category=0
    '''rounding scores to 3 decimal places because schema for difficulty_score is DECIMAL(10,3)
    in our table and converting it to float as currently it is np.float64'''
    if scores[i]<=low_cut:
        diff_category=1
    elif scores[i]>=high_cut:
        diff_category=3
    else:
        diff_category=2

    updates.append((float((round(scores[i],3))) , diff_category, list(map(float,embed[i])) ,  ids[i] )) 

cur.executemany(
    """
    UPDATE resources SET difficulty_score = %s, difficulty_category = %s , embedding = %s
    WHERE id = %s
    """,
    updates
)

conn.commit()


cur.close()
conn.close()