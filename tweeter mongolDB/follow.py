import sqlite3
import user
# Connect to the database
file = None
#conn = sqlite3.connect(file)
#cursor = conn.cursor()

def get_db(db):
    global file
    file = db
'''

def print_followers(followee):
    print("""
    ____________________________________________________________
    FOLLOWERS                                          
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++""")

    followerList = list_following(followee)

    for flwer in followerList:
        print(flwer)

def follow(follower, followee):
    # Follow a user
    cursor.execute("INSERT INTO follows (flwer, flwee, start_date) VALUES (?, ?, CURRENT_DATE)", (follower, followee))
    conn.commit()

def retriever_follower(user):
    cursor.execute("SELECT flwer FROM follows WHERE flwee = ?", (user))
    user = cursor.fetchall()

def list_following(user):
    follow_list = []
    index = 0
    for follower in retriever_follower(user):
        print(follower[0])
        follow_list.append(follower[0])
        index += 1
    return follow_list

def followers_info(followee ,follower: tuple):
    #user.print_user_string(user: tuple, is_detailed=True)
    #user.display_users(user: tuple, quantity: int=5)
    ans = input("Do you want to follow this user? y/n (if yes type y if not print n)")
    if ans.lower() == 'y':
        follow(followee, follower[0])
        return 1
    else:
        return 0
    
conn.close()


'''
