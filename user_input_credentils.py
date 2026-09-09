import psycopg2
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

def server():
    #connecting to postgres
    conn = psycopg2.connect(
        host="localhost",
        database="recommander_system",
        user='postgres',
        password="Sachin1130!",
        port=5432
    )

    return conn

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

    cur.close()
    conn.close()

    return user_id
    


def sign_up():
    user_name = input("Enter user name: ")
    user_email = input("Enter your email: ")
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
    
