''' 
difficulty_fit rules:
gap = resource_level - user_level
if gap == 0 -> 1.0
if gap == 1 -> 0.5
if gap <= -1 -> 0.2
if gap >= 2 -> reject resource
'''
#this fucntion will return difficulty gap between user level and current resource
#based on above rules
def gap(user_diff,resource_diff): 

    gap=resource_diff-user_diff

    if gap==0:
        return 1
    elif gap==1:
        return 0.5
    elif gap<=-1:
        return 0.2
    else:   #gap >= 2
        return 0 #0 means reject resource


#this is main function in here, it takes dict of user profile, and 
#list of dicts of resources and call gap function for each resource and 
#make a new dictionary with resource id as key, score as value and returns it
def difficulty_gap(user_profile,resources):
    resource_score={} #this will contain resource id as key and difficulty score as value
    user_level=user_profile["current_level"]

    for resource in resources:
        score=gap(user_level,resource["difficulty_level"])
        if score==0:  #if score==0 i.e gap is too large then just donot put resource in dict
            continue
        resource_score[resource["id"]] = score

    
    return resource_score


