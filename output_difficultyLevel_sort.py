#if user difficulty score is 1, then output should be -> 1,2,3; if user difficulty score is 2, then output should be -> 2,3,1; if difficulty score is 3, then output should be -> 3,2,1

def user_is_begineer(resources):
    return sorted(resources, key=lambda x: x["difficulty_category"])

def user_is_intermediate(resources):
    print(resources)
    print(resources[0])
    print(type(resources[0]))
    sorted_list=sorted(resources, key=lambda x: x["difficulty_category"]) #got a sorted list, now just ned to get level 1 to after level 3

    count_of_level1=0
    resources_of_level1=[]
    for i in range(len(sorted_list)): #getting resources of level 1

        if sorted_list[i]["difficulty_category"]==1:
            count_of_level1+=1
            resources_of_level1.append(sorted_list[i])
        
        else:
            break

    sorted_list.extend(resources_of_level1)  #copying level 1 to end
    return sorted_list[count_of_level1:]  #returning resources of level 2 -> 3 -> 1


def user_is_advanced(resources):
    return sorted(resources, key=lambda x: x["difficulty_category"], reverse=True)

