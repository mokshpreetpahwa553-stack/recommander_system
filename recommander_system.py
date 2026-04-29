#from user_resource_difficulty import difficulty_gap
from goal_topic_similarity import similarity
from fetch_youtubeVids import fetch_youtubeVideos
from colorama import init , Fore
import numpy as np
def recommander(resources,user_profile):

    #diff_score=difficulty_gap(user_profile,resources) #dict, with real ids as key and score as value
    #viable_opt=list(diff_score.keys()) #this list contains ids of all resources which are viable(difficulty is not too high)
    viable_resource=[]
    #viable_resources_with_diff=[]

    for resource in resources:
        if resource["difficulty_category"] == user_profile["current_level"]:
            viable_resource.append(resource)
            

    #sim_res_value is list of tuples with idx and cosine sim value in desc order
    sim_res_value=similarity(viable_resource,user_profile)

    combined_results=[]

    #we created a formula
    #similarity matters 0.6% ; topic matters most
    #preference matters 0.1%
    for pair in sim_res_value:
        idx=pair[0]
        if viable_resource[idx]["format"]==user_profile["resource"]:  #if preference amtch then preference score is 1
            p=1.00
        else:   #otherwise 0.2
            p=0.2
        
        score=(0.6 * pair[1]) + (0.4 * p) #+ (0.3 * diff_score[viable_resource[idx]["id"]])
        combined_results.append((idx,score))

    sorted_combined_results=sorted(combined_results,key=lambda x: x[1],reverse=True)[:10] #sort acc to result in desc order then take top 20
    #sorted_along_diff=sorted(sorted_combined_results, key=lambda x:viable_resource[x[0]]["difficulty_level"]) #sorting according to difficulty level for dictionaries in viable resources

    #sorted_acc_score_within_distances=[] #empty list, it will contain list of tuples with sorted along score in desc order, within each difficulty level

    i=0
   #while i<len(sorted_along_diff):
    '''idx=sorted_along_diff[i][0]
        j=i+1
        same_difficulty=[]  #this will contain tupes having same resource difficulty level, it always initializes to empty on start of new difficulty level
        same_difficulty.append(sorted_along_diff[i])  #we always appendd first tuple of new difficulty level
        while j<len(sorted_along_diff) and (viable_resource[idx]["difficulty_level"]==viable_resource[sorted_along_diff[j][0]]["difficulty_level"]):  #checking for j<total len of list and difficulty level of next resources
            same_difficulty.append(sorted_along_diff[j])   #we append if difficulty is same
            j+=1  #incrementing j
        
        sort_scores=sorted(same_difficulty,key=lambda x:x[1],reverse=True) #sorting scores 
        sorted_acc_score_within_distances.extend(sort_scores)   #then putting them in sorted_acc_score_within_distances, sorted according to scores within each difficulty
        i=j   '''
    

    recommanded=[]
    #for pair in sorted_acc_score_within_distances[:10]:  #out of 20 show top 10
    #   idx=pair[0]
    #  recommanded.append(viable_resource[idx])'''
    for pair in sorted_combined_results[:10]:
        idx=pair[0]
        recommanded.append(viable_resource[idx])
    
    return recommanded
        

def user_profiling(goal,level,pref_format):
    #following list would contain keywords that would map up intent of user
    practice_intent=["quiz","question","test","practice","challenge","sheet"]
    understand_intent=["understand","why","explain","concept","theory"]
    examprep_intent=["sat","exam","jee","test prep","advance","neet","gcse"]
    puzzle_intent=["puzzle","riddle","brain","teaser","iq"]

    UNKNOWN,practice,understand,exam_prep,puzzle=0,0,0,0,0

    words=goal.lower().split()
    for g in words:
        if g in practice_intent:
            practice+=1
        elif g in understand_intent:
            understand+=1
        elif g in examprep_intent:
            exam_prep+=1
        elif g in puzzle_intent:
            puzzle+=1
    
    intents=["UNKNOWN","practice","understand","exam_prep","puzzle"]

    max_intent=np.argmax([UNKNOWN,practice,understand,exam_prep,puzzle])
    intent=intents[max_intent]


    user_profile={
        "goal": goal,
        "current_level": level,
        "resource": pref_format,
        "intent": intent,
    }
    print(user_profile)
    return user_profile



if __name__=="__main__":

    init(autoreset=True)
    #taking input for goal 
    goal=input("Enter goal: ")

    #taking current level, prompting user until user enters value 1-3
    while True:
        try:
            current_level=int(input("Enter your current level(1-Begineers, 2-Intermediate, 3-Advanced): "))
            if current_level>=1 and current_level<=3:
                break

            else:
                print("Enter value between 1 and 3")

        except ValueError:
            print("Enter integer value")

    #we support these resource only
    available_resources=["videos","course","article","research paper"]

    while True:
        resource=input(f"Enter preffered resource{available_resources}: ")
        
        if resource in available_resources:
            break
        else:
            print("This resource type is not supported")


    user_profile=user_profiling(goal,current_level,resource)

    level=["begineer","intermediate","advanced"]
    modifiedgoal=goal+" "+level[current_level-1]
    
    resources = fetch_youtubeVideos(modifiedgoal)
    recommandations=[]
    if resources:
        recommandations=recommander(resources,user_profile)
    else:
        print("No resources")

    print("\n")
    for r in recommandations:
        print(f"{Fore.MAGENTA}id: {Fore.WHITE}{r.get('id','')}\n"
              f"{Fore.MAGENTA}title: {Fore.WHITE}{r.get('title','')}\n"
              f"{Fore.MAGENTA}title: {Fore.WHITE}{r.get('topic','')}\n"
              f"{Fore.MAGENTA}description: {Fore.WHITE}{r.get('description','')}\n"
              f"{Fore.MAGENTA}difficulty_score: {Fore.WHITE}{r.get('difficulty_score','')}\n"
              f"{Fore.MAGENTA}difficulty_level: {Fore.WHITE}{r.get('difficulty_category','')}\n"
              f"{Fore.MAGENTA}format: {Fore.WHITE}{r.get('format','')}\n"
              f"{Fore.MAGENTA}URL: {Fore.WHITE}{r.get('url','')}\n"
              f"{Fore.MAGENTA}languag: {Fore.WHITE}{r.get('language','')}\n\n")


        
        
    #all available resources
    '''resources = [
    {
        "id": "res_1",
        "title": "Python Basics Crash Course",
        "description": "Intro to Python syntax, variables, conditionals, and loops for absolute beginners.",
        "topic": "python_basics",
        "difficulty_level": 1,
        "format": "course",
        "url": "https://example.com/python-basics-crash-course",
        "source": "example_courses",
        "est_duration_min": 180,
        "language": "en",
    },
    {
        "id": "res_2",
        "title": "Learn Python by Writing Small Scripts",
        "description": "Hands-on guide focused on small automation scripts, input/output, and basic error handling.",
        "topic": "python_basics",
        "difficulty_level": 1,
        "format": "article",
        "url": "https://example.com/python-small-scripts",
        "source": "example_blog",
        "est_duration_min": 45,
        "language": "en",
    },
    {
        "id": "res_3",
        "title": "Beginner-Friendly Python Video Series",
        "description": "Video playlist covering installing Python, using a REPL, and writing your first programs.",
        "topic": "python_basics",
        "difficulty_level": 1,
        "format": "video",
        "url": "https://example.com/python-video-series",
        "source": "example_video_platform",
        "est_duration_min": 120,
        "language": "en",
    },
    {
        "id": "res_4",
        "title": "Practical Pandas for Data Analysis",
        "description": "Intermediate tutorial on DataFrames, indexing, filtering, groupby, and basic joins.",
        "topic": "pandas",
        "difficulty_level": 2,
        "format": "article",
        "url": "https://example.com/practical-pandas",
        "source": "example_blog",
        "est_duration_min": 60,
        "language": "en",
    },
    {
        "id": "res_5",
        "title": "Pandas Essentials Mini-Course",
        "description": "Project-based course using Pandas for cleaning and exploring real-world datasets.",
        "topic": "pandas",
        "difficulty_level": 2,
        "format": "course",
        "url": "https://example.com/pandas-essentials-course",
        "source": "example_courses",
        "est_duration_min": 240,
        "language": "en",
    },
    {
        "id": "res_6",
        "title": "Data Manipulation with Pandas (Video)",
        "description": "Intermediate screencast on reshaping, merging, and time series basics with Pandas.",
        "topic": "pandas",
        "difficulty_level": 2,
        "format": "video",
        "url": "https://example.com/pandas-data-manipulation-video",
        "source": "example_video_platform",
        "est_duration_min": 90,
        "language": "en",
    },
    {
        "id": "res_7",
        "title": "Introduction to Machine Learning in Python",
        "description": "Covers train/test splits, basic models, and evaluation using scikit-learn.",
        "topic": "ml_basics",
        "difficulty_level": 2,
        "format": "course",
        "url": "https://example.com/ml-intro-python",
        "source": "example_courses",
        "est_duration_min": 300,
        "language": "en",
    },
    {
        "id": "res_8",
        "title": "Advanced Deep Learning Architectures",
        "description": "Research-oriented overview of modern neural network architectures and training tricks.",
        "topic": "ml_advanced",
        "difficulty_level": 3,
        "format": "paper",
        "url": "https://example.com/advanced-deep-learning-paper",
        "source": "example_research",
        "est_duration_min": 90,
        "language": "en",
    },
    {
        "id": "res_9",
        "title": "Hands-on Project: Build a Recommender in Python",
        "description": "Step-by-step project implementing a simple recommendation system with Pandas and matrix factorization.",
        "topic": "ml_advanced",
        "difficulty_level": 3,
        "format": "article",
        "url": "https://example.com/build-recommender-python",
        "source": "example_blog",
        "est_duration_min": 120,
        "language": "en",
    },
    {
        "id": "res_10",
        "title": "Research Paper Recommender Systems: A Literature Survey",
        "description": "Survey paper reviewing more than 200 research-paper recommender systems, summarizing common algorithms, evaluation methods, and open challenges.",
        "topic": "ml_advanced",
        "difficulty_level": 3,
        "format": "paper",
        "url": "https://example.com/research-paper-recommender-systems-survey",
        "source": "example_research",
        "est_duration_min": 150,
        "language": "en",
    },
    ]


    #creating user profile dictionary, it contains info about user
    user_profile={
        'goal': goal,
        'current_level': current_level,
        'resource': resource
    }'''


