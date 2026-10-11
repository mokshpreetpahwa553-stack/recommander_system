from user_input_credentials import sign_in,sign_up
from recommander_system import recommanderSystem
import psycopg2
import sys
#connecting to postgres
conn = psycopg2.connect(
    host="localhost",
    database="recommander_system",
    user='postgres',
    password="Sachin1130!",
    port=5432
)

cur=conn.cursor()

if __name__ == "__main__":
    user_choice = input("If you have an account->sign_in, otherwise sign_up or use as guest: ")

    if user_choice == "sign_in":
        while True:
            userId=sign_in()
            if userId!=-1:
                break

    elif user_choice=="sign_up":
        sign_up()
        userId=sign_in()

    elif user_choice=="guest":
        recommanderSystem()

    #password entered incorrect for 3 times 
    if userId=="incorrect password limit":
        print("incorrect password limit\nTry again later!!\n\n")
        sys.exit()

    while True:
        choice = input("\n\n1 - recommander_system\n2 - View search history\n3 - Quit\nINPUT :")

        if choice=="1":
            query,resource_type_used=recommanderSystem()
            cur.execute(
                """
                INSERT INTO query_history(user_id,query_text,resource_type_used) VALUES(%s,%s,%s)""",
                (userId,query,resource_type_used)
            )

            conn.commit()

        elif choice=="2":
            cur.execute("""
                SELECT query_text,resource_type_used FROM query_history WHERE user_id = %s ORDER BY time_created DESC""",
                (userId,))

            queries = cur.fetchall()

            for query in queries:
                print(f"{query[0]}\t{query[1]}")

            conn.commit()

        elif choice=="3":
            print("THANKS!!")
            break

    

    cur.close()
    conn.close()
    

        