from sentence_transformers import SentenceTransformer
import numpy as np

model=SentenceTransformer("all-MiniLM-L6-v2")

def texts_from_resources(resources): #it put overview of each resource into a single list
    text=[]
    for resource in resources:
        text.append(resource["title"]+" "+resource["description"]+" ")
    
    return text

def embedding(text): #function to return embeddings
    return model.encode(text,normalize_embeddings=True)


def similarity(resources,user_profile):
    whole_text=texts_from_resources(resources)

    resource_emb=embedding(whole_text)
    
    user_goal=[]
    user_goal.append(user_profile["goal"]) #making user goal in a list, bcs embedding expects list of stirng

    user_emb=embedding(user_goal)[0] #we took first row bcs after embedding we will get 2-D array in shape(1,384) so to get first row(only useful row bcs our emb is like [[48 84 654 44   5 545 54 4 8 7]])
  
    # normalize
    resource_norms = np.linalg.norm(resource_emb, axis=1, keepdims=True)
    user_norm = np.linalg.norm(user_emb)

        # avoid division by zero
    resource_emb_norm = resource_emb / (resource_norms + 1e-10)
    user_emb_norm = user_emb / (user_norm + 1e-10)

    sims=np.dot(resource_emb_norm,user_emb_norm)  #cosine similarity

    index_sims=[] #list contain index of resourses as index and value as similarity value
    for idx,s in enumerate(sims):
        index_sims.append((idx,s))
    

    return sorted(index_sims,key=lambda x:x[1],reverse=True) #, np.argsort(sims)[::-1]  #returning list of tuples with index of resouce and similarity value in desc order and index of resources in descending order
 


