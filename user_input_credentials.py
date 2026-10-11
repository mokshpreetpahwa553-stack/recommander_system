import psycopg2
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import string
from colorama import init , Fore
import os
from dotenv import load_dotenv

ph = PasswordHasher()

def server():
    load_dotenv()
    DATABASE_PASS = os.getenv("DATABASE_PASSWORD")

    #connecting to postgres
    conn = psycopg2.connect(
        host="localhost",
        database="recommander_system",
        user='postgres',
        password=DATABASE_PASS,
        port=5432
    )


    return conn

def password_checker(password): #this function will tell if password is good or not
    init(autoreset=True)
    if len(password)<6:
        print("> Password length must be 7")

    good_password=True

    if not any(i in string.ascii_uppercase for i in password):
        print(f"{Fore.RED}> Add atleast one Uppercase Letters")
        good_password=False
    
    if not any(i in string.ascii_lowercase for i  in password):
        print(f"{Fore.RED}> Add lowercase letters")
        good_password=False
       
    if not any(i in string.digits for i in password):
        print(f"{Fore.RED}> Add atleast one digit")
        good_password=False
      
    if not any(i in string.punctuation for i in password):
        print(f"{Fore.RED}> Add atlesat 1 special character")
        good_password=False

    return good_password


def sign_in():
    user_email = input("Enter your email: ")
    user_password = input("Enter password: ")
    conn=server()
    
    cur=conn.cursor()

    cur.execute(
        """
        SELECT user_id,password_hash FROM users WHERE email = %s
        """,(user_email,)  #used (user_email,) and not (user_email) bcs .execute expects a tuple and (user_email) is a str datatype
    )

    result = cur.fetchone() #fetchone returns a tuple
    if result is None:
        print("Email not found")
        return -1
    else:
        user_id,user_original_password=result

        count=0
        while count<3:
            try:
                if count>0:
                    user_password = input("Enter password: ")
                ph.verify(user_original_password,user_password)
                print("Login successfully!!")
                break

            except VerifyMismatchError:
                print("Incorrect Password")
                count+=1
                if count==3:
                    return "incorrect password limit"

    cur.close()
    conn.close()

    return user_id
    


def sign_up():
    user_name = input("Enter user name: ")
    user_email = input("Enter your email: ")
    user_password = input("Enter password: ")

    while True:  #if password is good enough then alright otherwise write new password
        if password_checker(user_password):
            break

        user_password = input("Enter password: ")

    
    hashed_password=ph.hash(user_password)

    conn=server()
    
    cur=conn.cursor()
    
    cur.execute(
        '''
        INSERT INTO users(username,email,password_hash) 
        VALUES (%s,%s,%s)''', (user_name,user_email,hashed_password)
    )

    print("Account made successfully!!")
    conn.commit()

    cur.close()
    conn.close()
    
