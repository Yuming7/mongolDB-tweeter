import sqlite3
from tweet import display_tweets, print_tweet_string
#from search import display
file = None
conn = None
c = None


def set_file1(filename) -> None:
    global file, c, conn
    file = filename
    conn = sqlite3.connect(file)
    c = conn.cursor()

# def print_user_string(user: tuple, is_detailed: bool = False) -> None: 
#     """
#     print_user_string(user: tuple, is_detailed: bool = False) -> list (displayed tweets)

#     Prints a user string (usr,pwd, name,email,city,timezone) in the following format:

#     is_detailed = False:
#     ------------------------------------------------------------
#     name                                                    city
    
#     is_detailed = True:
#     ------------------------------------------------------------
#     name                                                    city
#     @user_id

#     no_posts posts    no_flwer following    no_flwee followers
#     ------------------------------------------------------------
#     print_tweet_string(tweet1)
#     ------------------------------------------------------------
#     print_tweet_string(tweet2)
#     ------------------------------------------------------------
#     print_tweet_string(tweet3)

#     """
#     # conn = sqlite3.connect(FILENAME)
#     # c=conn.cursor()
#     (usr,pwd,name,email,city,timezone) = user
#     print(60*"-")
#     print(f"{name:<40}{city:>20}")
#     if is_detailed == True:
#         print(f"@{usr}\n")
#         c.execute("SELECT COUNT(*) FROM tweets WHERE writer=%d;"%(usr))
#         posts=c.fetchone()[0]
#         #print(f"{posts} posts\n\n")
#         c.execute("SELECT COUNT(*) FROM follows WHERE flwer=%d;"%(usr))
#         following=c.fetchone()[0]
#         c.execute("SELECT COUNT(*) FROM follows WHERE flwee=%d;"%(usr))
#         followers=c.fetchone()[0]
#         print(f"\n{posts} posts    {following} following    {followers} followers")
#         c.execute("SELECT * FROM tweets WHERE writer=%d ORDER BY tdate DESC;"%(usr))
#         tweets = c.fetchall()
#         display(tweets,"t",3)
        

    
def display_users(users: list, quantity: int=5) -> list:
    """
    display_users(users: list[tuple], quantity: int=5) -> list

    Displays users usr,pwd, name,email,city,timezone at 
    specified increment (quantity) and returns a list of tuples 
    of the displayed users so they can be selected for more detail. 
    First user displayed is index 1 in the list.
    """
    show_more = True
    index = 0
    displayed_users = [0]
    
    while show_more == True:
        for i in range(quantity):
            if i+index == len(users):
                print(" End of Users ".center(60,"-")+"\n")
                show_more = False
                break
            else:
                user = users[i+index]
                displayed_users.append(user)
                print_user_string(user)
                i+=1
        if show_more == True:
            show_more = input("Show More?(y/n) ")
            while show_more.lower() not in ["y","n"]:
                show_more = input("Invalid Input. Show More?(y/n) ")
            if show_more.lower() == "n":
                show_more == False
            else:
                show_more=True
                index+=quantity
    return displayed_users

def main():
    # conn = sqlite3.connect(FILENAME)
    # c=conn.cursor()
    c.execute("SELECT * FROM users;")
    users=c.fetchall()
    display_users(users)
    c.execute("SELECT * FROM users WHERE usr=%d"%(20))
    user=c.fetchone()
    print_user_string(user,True)

#main()
