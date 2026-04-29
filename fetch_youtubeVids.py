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

    #following keywords are used to map topic to each resource video
    algebra_keywords=["algebra", "equation", "equations", "solve", "x", "linear", "quadratic", "polynomial", "factor", "factoring", "root", "roots", "expression", "simultaneous", "system","equations"]
    arithmetic_mental_math_keywords=["arithmetic", "addition", "subtraction", "multiplication", "division", "mental"," math", "mentalmath", "trick", "tricks", "shortcut", "shortcuts", "fast", "faster", "speed"]
    calculus_keywords=["calculus", "derivative", "derivatives", "integral", "integrals", "integration", "differentiate", "differentiation", "limit", "limits", "d/dx", "antiderivative", "chain"]
    geometry_keywords=["geometry", "triangle", "triangles", "circle", "circles", "area", "perimeter", "angle", "angles", "polygon", "square", "rectangle", "coordinate", "coordinates", "shape", "shapes"]
    probability_stats_keywords=["probability", "statistics", "statistic", "stats", "random", "chance", "permutation", "permutations", "combination", "combinations", "binomial", "distribution", "expectation", "mean", "median", "variance"]
    number_theory_keywords=["number theory", "prime", "primes", "divisible", "divisibility", "mod", "modulo", "remainder", "gcd", "lcm", "factorization"]
    puzzles_brainteasers_keywords=["puzzle", "puzzles", "riddle", "riddles", "brain teaser", "brain","teasers", "brain-teaser", "test", "iq", "logic","puzzle", "puzzles", "brainteaser", "challenge", "challenging","riddle"]
    exam_prep_keywords=["sat", "gcse", "neet", "jee", "exam", "exams", "prep", "preparation", "paper", "papers", "mock", "practice" ,"test", "official exam", "math","section"]
    olympiad_competition_keywords=["olympiad", "imo", "amc", "aime", "contest", "competition", "hardest","problem"]
    general_math_keywords=["math", "maths", "mathematics"]


    topic_keywords={
        "algebra": algebra_keywords,
        "arithmetic_mental_math": arithmetic_mental_math_keywords,
        "calculus": calculus_keywords,
        "general_math": general_math_keywords,
        "probability_stats": probability_stats_keywords,
        "number_theory": number_theory_keywords,
        "geometry": geometry_keywords,
        "puzzles_brainteasers": puzzles_brainteasers_keywords,
        "exam_prep": exam_prep_keywords,
        "olympiad_competition": olympiad_competition_keywords,
    }
    
    full_text_of_each_video=[]
    for item in items:
        vid=item["id"]["videoId"]
        snip=item["snippet"]
        title=snip["title"]
        desc=snip.get("description","")
        channel=snip.get("channelTitle","")

        full_text_of_each_video.append((title+" "+desc).lower())

        topic_counts={
        "UNKNOWN": 0,
        "algebra": 0,
        "arithmetic_mental_math": 0,
        "calculus": 0,
        "general_math": 0,
        "probability_stats": 0,
        "number_theory": 0,
        "geometry": 0,
        "puzzles_brainteasers": 0,
        "exam_prep": 0,
        "olympiad_competition": 0,
    }
    
       
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
            "est_duration_min": 0,
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


