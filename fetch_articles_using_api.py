import requests
import hashlib
import joblib
import numpy as np
NEWS_API_KEY = '44fb3233ded44c939c7a2945222f4f7a'

def newsapi_items_to_resources(items):
    print("Entered in conversion!")
    resources=[]
    full_text_of_each_article = []

    for article in items:
        title=article.get("title","")
        desc = article.get("description","")
        url = article.get("url","")
        source = article.get("source", {}).get("name", "")
        content=article.get("content","")
        full_text_of_each_article.append((title + " " + desc).lower())
        
        article_id = "art_" + hashlib.md5(url.encode()).hexdigest()[:10]

        resources.append({
                "id": article_id,
                "title": title,
                "description": desc,
                "difficulty_score": None,
                "difficulty_category": None,
                "format": "article",
                "url": url,
                "source": source,
                "language": "en",
            })
        

    #full_text_of_each_article=full_text_of_each_article.lower()
        # Load model once when program starts
    model = joblib.load('text_scorer_pipeline.pkl')
    scores=model.predict(full_text_of_each_article)
    minscore=min(scores)
    maxscore=max(scores)
    print(f"maxscore->{maxscore}")
    print(f"minscore->{minscore}")

    #normalising scores
    scores = scores-scores.mean()/scores.std()
    scores = np.array(scores)
    low_cut = np.percentile(scores, 33)
    high_cut = np.percentile(scores, 67)

    #assigining categories on predicted score by linear regression model
    for i in range(len(scores)):
        resources[i]["difficulty_score"]=scores[i]
        if scores[i]<=low_cut:
            resources[i]["difficulty_category"]=1
        elif scores[i]>=high_cut:
            resources[i]["difficulty_category"]=3
        else:
            resources[i]["difficulty_category"]=2

    print("conversion done")
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
        "pageSize": min(max_results, 100),
    }

    headers = {
        "X-Api-Key": NEWS_API_KEY
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()

        if not data.get("articles"):
            print(f"No article results for '{query}'")
            return []

        print("TO next func")
        return newsapi_items_to_resources(data["articles"])

    except Exception as e:
        print(f"ARTICLE API ERROR: {e}")
        return []