#from user_resource_difficulty import difficulty_gap
from goal_topic_similarity import similarity
from fetch_yt_from_postgres  import fetch_resources
#from fetch_articles import fetch_articles
from colorama import init , Fore
import numpy as np
from output_difficultyLevel_sort import user_is_begineer, user_is_intermediate, user_is_advanced


def recommander(resources,user_profile):

    #diff_score=difficulty_gap(user_profile,resources) #dict, with real ids as key and score as value
    #viable_opt=list(diff_score.keys()) #this list contains ids of all resources which are viable(difficulty is not too high)
    #viable_resource=[]
    #viable_resources_with_diff=[]

    '''for resource in resources:
        if resource["difficulty_category"] == user_profile["current_level"]:
            viable_resource.append(resource)'''
            

    #sim_res_value is list of tuples with idx and cosine sim value in desc order
    resources_with_scores=similarity(resources,user_profile)

    #resources_with_scores=[]

    #we created a formula
    #similarity matters 0.6% ; topic matters most
    #preference matters 0.1%
    '''for pair in sim_res_value:
        idx=pair[0]
        if resources[idx]["format"]==user_profile["resource"]:  #if preference amtch then preference score is 1
            p=1.00
        else:   #otherwise 0.3
            p=0.3
        
        score=(0.6 * pair[1]) + (0.4 * p) #+ (0.3 * diff_score[viable_resource[idx]["id"]])
        combined_results.append((idx,score))
    '''

    #updating scores of resources
    for resource in resources_with_scores:
        if resource["format"]==user_profile["resource"]:  #if preference amtch then preference score is 1
            p=1.00
        else:   #otherwise 0.3
            p=0.3
        
        score=(0.6 * resource["score"]) + (0.4 * p) #+ (0.3 * diff_score[viable_resource[idx]["id"]])
        resource["score"]=score

    top_resources=sorted(resources_with_scores,key=lambda x: x["score"],reverse=True)[:10] #sort acc to result in desc order then take top 20
    

    '''sorted_along_diff=sorted(sorted_combined_results, key=lambda x:resources[x[0]]["difficulty_category"]) #sorting according to difficulty level for dictionaries in viable resources

    sorted_acc_score_within_distances=[] #empty list, it will contain list of tuples with sorted along score in desc order, within each difficulty level

    i=0
    while i<len(sorted_along_diff):
        idx=sorted_along_diff[i][0]
        j=i+1
        same_difficulty=[]  #this will contain tupes having same resource difficulty level, it always initializes to empty on start of new difficulty level
        same_difficulty.append(sorted_along_diff[i])  #we always appendd first tuple of new difficulty level
        while j<len(sorted_along_diff) and (resources[idx]["difficulty_category"]==resources[sorted_along_diff[j][0]]["difficulty_category"]):  #checking for j<total len of list and difficulty level of next resources
            same_difficulty.append(sorted_along_diff[j])   #we append if difficulty is same
            j+=1  #incrementing j
        
        sort_scores=sorted(same_difficulty,key=lambda x:x[1],reverse=True) #sorting scores 
        sorted_acc_score_within_distances.extend(sort_scores)   #then putting them in sorted_acc_score_within_distances, sorted according to scores within each difficulty
        i=j   

    recommanded=[]
    #for pair in sorted_acc_score_within_distances[:10]:  #out of 20 show top 10
    #   idx=pair[0]
    #  recommanded.append(viable_resource[idx])
    for pair in sorted_combined_results[:10]:
        idx=pair[0]
        recommanded.append(resources[idx])'''

    
    if user_profile["current_level"]==1:
        recommandations=user_is_begineer(top_resources)
    elif user_profile["current_level"]==2:
        recommandations=user_is_intermediate(top_resources)
    else:
        recommandations=user_is_advanced(top_resources)    

    '''i=0
        while i < len(recommandations):
        idx=recommandations[i][0]
        j=i+1
        same_difficulty=[]   
        same_difficulty.append(recommandations[i])
        while j<len(recommandations) and (resources[idx]["difficulty_category"]==resources[recommandations[j][0]]["difficulty_category"]):
            same_difficulty.append(recommandations[j])
            j+=1
        sort_scores=sorted(same_difficulty,key=lambda x:x[1],reverse=True)
        recommandations.extend(sort_scores)
        i=j
    '''

    i,j=0,0
    sorted_recommandations=[]
    
    while i < len(recommandations):
        while j < len(recommandations) and (recommandations[i]["difficulty_category"]==recommandations[j]["difficulty_category"]):
            j+=1
        sort_scores=sorted(recommandations[i:j],key=lambda x:x["score"],reverse=True)
        sorted_recommandations.extend(sort_scores)
        i=j

    return sorted_recommandations
        

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

    level=["beginner","intermediate","advanced"]
    modifiedgoal=f"{goal} for {level[current_level-1]} level"
    
    if resource=="videos":
        resources=fetch_resources()
        
    recommandations=[]
    
    if resources:
        recommandations=recommander(resources,user_profile)
    else:
        print("No resources")

    print("\n")
   
    for r in recommandations:
        print(f"{Fore.MAGENTA}title: {Fore.WHITE}{r.get('title','')}\n"
              f"{Fore.MAGENTA}description: {Fore.WHITE}{r.get('description','')}\n"
              f"{Fore.MAGENTA}difficulty_score: {Fore.WHITE}{r.get('difficulty_score','')}\n"
              f"{Fore.MAGENTA}difficulty_level: {Fore.WHITE}{r.get('difficulty_category','')}\n"
              f"{Fore.MAGENTA}format: {Fore.WHITE}{r.get('format','')}\n"
              f"{Fore.MAGENTA}URL: {Fore.WHITE}{r.get('url','')}\n"
              f"{Fore.MAGENTA}language: {Fore.WHITE}{r.get('language','')}\n\n")
