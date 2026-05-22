from googleapiclient.discovery import build
import numpy as np
import joblib
from sklearn.pipeline import Pipeline 

API_KEY="AIzaSyAHgsQZOa68pTMdhDAMr4GteG1-m8YLhAQ"
YOUTUBE_API_SERVICE_NAME="youtube"
YOUTUBE_API_VERSION='v3'

# Build a YouTube API client using the API key
youtube=build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=API_KEY)

def youtube_items_to_resources(items):
    resources=[]
    """
    Transform raw YouTube search API items into a list of 'resource' dicts
    used by the recommender."""
    
    full_text_of_each_video=[]
    for item in items:
        vid=item["id"]["videoId"]
        snip=item["snippet"]
        title=snip["title"]
        desc=snip.get("description","")
        channel=snip.get("channelTitle","")

        full_text_of_each_video.append((title+" "+desc).lower())    
       
        resources.append({
            "id": f"yt_{vid}",
            "title": title,
            "description": desc,
            #"topic": topic,
            "difficulty_score": None,
            "difficulty_category": None,
            "format": "video",
            "url": f"https://www.youtube.com/watch?v={vid}",
            "source": channel,
            "language": snip.get("defaultAudioLanguage", "en"),
        })

    
    # Load model once when program starts
    model = joblib.load('text_scorer_pipeline.pkl')
    scores=model.predict(full_text_of_each_video)
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

    return resources


def fetch_youtubeVideos(query: str, max_results=100):

    """
    Call YouTube Data API search.list to get video search results and
    convert them into our internal 'resource' dicts.

    query       : user search string, e.g. 'cooking for beginners'
    max_results : number of videos to retrieve (YouTube max is 50)
    """
    # Build the search request:
    #   part      = which fields to return (id + snippet)
    #   q         = search text
    #   type      = only videos (not channels/playlists)

    try:
        request = youtube.search().list(
            part="id,snippet",
            q=query,
            type="video",
            maxResults=max_results,
        )

        # Execute HTTP request and get JSON response as a Python dict
        response=request.execute()

        if not response.get('items'):
            print(f"No results for '{query}'")
            return [] 
        
        return youtube_items_to_resources(response["items"])
    
    except Exception as e:
        print(f"API ERROR: {e}")
        return []  # Safe fallback


