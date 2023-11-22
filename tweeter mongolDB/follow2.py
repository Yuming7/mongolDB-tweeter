import sqlite3
import user, search
file = 'test.db'
conn = sqlite3.connect(file)
c = conn.cursor()

def get_db(db):
    global file
    file = db

def get_my_followers(usr:int) -> list:
    c.execute("SELECT flwer FROM follows WHERE flwee=%d"%(usr))
    follower_ids = c.fetchall()
    followers=[]
    for i in range(len(follower_ids)):
        follower = follower_ids[i][0]
        followers.append(follower)
    return followers

def display_followers(user:tuple) -> None:
    print("""
    ____________________________________________________________
    FOLLOWERS                                          
    """)
    usr = user[0]
    c.execute("SELECT flwer FROM follows WHERE flwee=%d"%(usr))
    follower_ids = c.fetchall()
    followers=[]
    for i in range(len(follower_ids)):
        follower = follower_ids[i][0]
        c.execute("SELECT * FROM users WHERE usr=%d"%(follower))
        followers.append(c.fetchone())
    search.display(followers,"u")

def display_followees(user:tuple) -> None:
    print("""
    ____________________________________________________________
    FOLLOWING                                          
    """)
    usr=user[0]
    c.execute("SELECT flwer FROM follows WHERE flwee=%d"%(usr))
    followee_ids = c.fetchall()
    followees=[]
    for i in range(len(followee_ids)):
        followee = followee_ids[i][0]
        c.execute("SELECT * FROM users WHERE usr=%d"%(followee))
        followees.append(c.fetchone())
    search.display(followees,"u")
    
    

def get_my_followees(usr:int) -> None:
    c.execute("SELECT flwee FROM follows WHERE flwer=%d"%(usr))
    followee_ids = c.fetchall()
    followees=[]
    for i in range(len(followee_ids)):
        followee = followee_ids[i][0]
        followees.append(followee)
    return followees

def follow(usr: int, followee: int) -> None:
    # Follow a user
    try:
        c.execute("INSERT INTO follows (flwer, flwee, start_date) VALUES (%d, %d, CURRENT_DATE)"% (usr, followee))
        conn.commit()
    except:
        print("\nSorry, you already follow this user.")
