import random
import string


def view_menu():
    print("1. Generate password")
    print("2. Check password strength")
    print("3. Suggestion to make password stronger")
    print("4. Generate password and check strength")
    print("5. EXIT")

def check_pass(password):  #funtion to check strength of password
    points=0
    #firstly checking on length base, used elif bcs password can have one definite length
    common=False
    if password.lower()=='admin' or password.lower()=='password': #checking for common passwords if yes the just give it two oints
        points=2               #if ther is a common password found just give it 2 points ignoring other criteria
        common=True
    else: #if not increase one point 
        points+=1 

        
    if 6<=len(password)<9:
        points+=1
    elif 9<=len(password)<=10:
        points+=2
    elif len(password)>10:
        points+=3
    else:
        print("Password must be 6 characters long")
        return 0,False,False,common #return default value
    
    #now checking on character variety and giving feedbacks
    
    if any(i in string.ascii_uppercase for i in password):
        points+=1
    if any(i in string.ascii_lowercase for i  in password):
        points+=1
    if any(i in string.digits for i in password):
        points+=1
    if any(i in string.punctuation for i in password):
        points+=1   

    #now checking on complexity

    triplets=False
    sequential=False
    for i in range(len(password)-2):
        if password[i] == password[i+1] == password[i+2]: #there are no continuous 3 repeated characters
            triplets=True #if triplets found we flag it

        if ord(password[i]) == ord(password[i+1])-1 == ord(password[i+2])-2: #checking for (abc),(123)
            sequential=True

    if triplets==False: #if triplets not found +1 point
        points+=1
    
    if sequential==False:
        points+=1
    
  

    return points,triplets,sequential,common
    

def gen_pass(length):
    option=string.ascii_letters+string.digits+string.punctuation #it can choose from all letters,digits and punctuations
    password=[]
    while len(password)<length:
        password.append(random.choices(option)[0])

    result="".join(password)
    print(result)
    return result
    

'''def suggestion(password): #this function will give suggestion make password stronger
   
    points,triplets,sequential,common=check_pass(password)
    if len(password)<7:
        print("> Password length must be 7")
    
    if not any(i in string.ascii_uppercase for i in password):
        print("> Add atleast one Uppercase Letters")
    if not any(i in string.ascii_lowercase for i  in password):
        print("> Add lowercase letters")
    if not any(i in string.digits for i in password):
        print("> Add atleast one digit")
    if not any(i in string.punctuation for i in password):
       print("> Add atlesat 1 special character") '''

def suggestion(password): #this function will give suggestion make password stronger
   
    #points,triplets,sequential,common=check_pass(password)
    if len(password)<6:
        print("> Password length must be 7")

    uppercase,lowercase,digit,special_character = False,False,False,False

    while uppercase==False and lowercase==False and digit==False and special_character==False:
        if not any(i in string.ascii_uppercase for i in password):
            print("> Add atleast one Uppercase Letters")
            uppercase=True
        if not any(i in string.ascii_lowercase for i  in password):
            print("> Add lowercase letters")
            lowercase=True
        if not any(i in string.digits for i in password):
            print("> Add atleast one digit")
            digit=True
        if not any(i in string.punctuation for i in password):
            print("> Add atlesat 1 special character")
            special_character=True
   

def gen_pass_check_str(length):  #this function will generate and check password 
   p= gen_pass(length)
   points,triplets,sequential,common=check_pass(p)
   return points

#main function
while True:
    print("\n")
    view_menu()
    print("\n")
    option=int(input("Choose an option: "))
    if option==1:
        password_length=int(input("How long password do you need: "))
        gen_pass(password_length)

    elif option==2:
        password=input("Enter password to check: ")
        points,triplets,sequential,common=check_pass(password)
         #printing result
        if 0<=points<=3:
            print("strength: weak")
        elif 4<=points<=7:
            print("strength: Medium")
        elif 8<=points<=10:
            print("strength: Strong")
    
    elif option==3:
        password=input("Enter password: ")
        suggestion(password)
                    
    elif option==4:
        password_length=int(input("How long password do you need: "))
        points= gen_pass_check_str(password_length)
         
         #printing result
        if 0<=points<=3:
            print("strength: weak")
        elif 4<=points<=7:
            print("strength: Medium")
        elif 8<=points<=10:
            print("strength: Strong")
            
    elif option==5:
        print("Good Bye")
        break
    
    else:
        print("Invalid input, choose between 1,2 and 3")
        
