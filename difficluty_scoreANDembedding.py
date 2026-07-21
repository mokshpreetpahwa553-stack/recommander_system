import joblib
import numpy as np
from sentence_transformers import SentenceTransformer
import time

from db_config import get_connection

def difficulty_score():
    #fetching all resources
    conn = get_connection()

    cur=conn.cursor()

    cur.execute(
        """
        SELECT display_id,title,description FROM resources 
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
    if scores.std()==0:
        scores=scores-scores.mean()
    else:
        scores = (scores-scores.mean())/scores.std()

    low_cut = np.percentile(scores, 33)
    high_cut = np.percentile(scores, 67)

    updates=[]
    j=0
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

        updates.append((float((round(scores[i],3))) , diff_category, ids[i] )) 
        print(f"row {j} score done")
        j+=1

    print("loop done")

    start = time.time()
    cur.executemany(
        """
        UPDATE resources SET difficulty_score = %s, difficulty_category = %s 
        WHERE display_id = %s
        """,
        updates
    )
    end=time.time()
    print("executemany done")
    print(f"total time in difficulty score execute many = {end-start:.2f} seconds" )
    conn.commit()
    print("DONE!!")

    cur.close()
    conn.close()

model=SentenceTransformer("all-MiniLM-L6-v2")
def embedding(resources):
    full_text=[]
    
    for resource in resources:
        if len(resource)<8:
            print(resource)
            continue
        full_text.append((resource[0]+' ' + resource[1]).lower())

    #now enbeddings of each row
    embed = model.encode(full_text,normalize_embeddings=True)

    return embed


if __name__=='__main__':
    difficulty_score()