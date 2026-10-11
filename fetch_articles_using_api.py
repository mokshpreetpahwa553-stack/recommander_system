import requests
import hashlib
import joblib
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ARTICLES_API_KEY")

if not API_KEY:
    raise ValueError("Missing ARTICLE_API_KEY. Add it to your .env file.")

def newsapi_items_to_resources(items):
    print("Entered in conversion!")
    resources=[]
    full_text_of_each_article = []

    for article in items:
        title=article.get("title") or ""
        desc = article.get("description") or ""
        url = article.get("url","")
        source = article.get("source", {}).get("name", "")
        content=article.get("content","")
        full_text_of_each_article.append((title + " " + desc).lower())
        language=article.get("language","en")
        #article_id = "art_" + hashlib.md5(url.encode()).hexdigest()[:10]

        resources.append((title,desc,"article",None,None,url,source,language))

        

    """#full_text_of_each_article=full_text_of_each_article.lower()
        # Load model once when program starts
    model = joblib.load('text_scorer_pipeline.pkl')
    scores=model.predict(full_text_of_each_article)
    minscore=min(scores)
    maxscore=max(scores)
    print(f"maxscore->{maxscore}")
    print(f"minscore->{minscore}")

    print("bnormal")
    #normalising scores
    scores = scores-scores.mean()/scores.std()
    scores = np.array(scores)
    low_cut = np.percentile(scores, 33)
    high_cut = np.percentile(scores, 67)
    print("anormal")
    #assigining categories on predicted score by linear regression model
    for i in range(len(scores)):
        resources[i]["difficulty_score"]=scores[i]
        if scores[i]<=low_cut:
            resources[i]["difficulty_category"]=1
        elif scores[i]>=high_cut:
            resources[i]["difficulty_category"]=3
        else:
            resources[i]["difficulty_category"]=2

    print("conversion done")"""
    return resources

def fetch_articles(query: str, max_results=100):
    """
    Call NewsAPI /v2/everything to get article search results and
    convert them into our internal 'resource' dicts.

    query       : user search string, e.g. 'cooking for beginners'
    max_results : number of articles to retrieve
    """
    print("Entered api func!")
    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": min(max_results, 50),
    }

    headers = {
        "X-Api-Key": NEWS_API_KEY
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()

        if not data.get("articles"):
            return f"No article results for '{query}'"
            

        print("TO next func")
        return newsapi_items_to_resources(data["articles"])

    except Exception as e:
        print(f"ARTICLE API ERROR: {e}")
        return []