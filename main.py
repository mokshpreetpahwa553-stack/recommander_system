from googleapiclient.discovery import build

API_KEY="AIzaSyAHgsQZOa68pTMdhDAMr4GteG1-m8YLhAQ"
YOUTUBE_API_SERVICE_NAME="youtube"
YOUTUBE_API_VERSION='v3'

youtube=build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=API_KEY)

def youtube_items_to_resources(items):
    resources=[]
    for item in items:
        vid=item["id"]["videoId"]
        snip=item["snippet"]
        title=snip["title"]
        desc=snip.get("description","")
        channel=snip.get("channelTitle","")

        difficulty_level=1

        resources.append({
            "id": f"yt_{vid}",
            "title": title,
            "description": desc,
            "difficulty_level": difficulty_level,
            "format": "video",
            "url": f"https://www.youtube.com/watch?v={vid}",
            "source": channel,
            "est_duration_min": 0,
            "language": snip.get("defaultAudioLanguage", "en"),
        })

    return resources


def fetch_youtubeVideos(query: str, max_results=10):
    try:
        request = youtube.search().list(
            part="id,snippet",
            q=query,
            type="video",
            maxResults=max_results,
            safeSearch="moderate",
        )

        response=request.execute()
        print(f"API returned {len(response.get('items', []))} videos")  # DEBUG

        if not response.get('items'):
            print(f"No results for '{query}'")
            return [] 
        return youtube_items_to_resources(response["items"])
    
    except Exception as e:
        print(f"API ERROR: {e}")
        return []  # Safe fallback


