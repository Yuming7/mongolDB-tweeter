import sqlite3, sys
import tweet

file, usr, c, conn = None, None, None, None

def set_user(username):
    global usr 
    usr = username

def set_db(db):
    global file, c, conn
    file = db
    conn = sqlite3.connect(file)
    c = conn.cursor()

def close_db():
    conn.close()

def show_tweet_options(tweetInfo):
    option = str(input("""
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    OPTIONS:
        1. Reply        
        2. Retweet 

        (H) Go back to feed
    ____________________________________________________________
    What would you like to do?  """))

    if option == "1":
        #print("placeholder: reply to tweet")
        tweet.compose_tweet(usr,tweetInfo[0])
        return True
    elif option == "2":
        print("placeholder: retweet function")

    elif option.upper() == "H":
        print(
    """[Returning to Dashboard]""")
        return False
    
def show_tweet_info(tweetID, mode = None):
    
    c.execute("SELECT * FROM tweets WHERE tweets.tid = %d" % (tweetID))
    tweetInfo = c.fetchone()

    tweet.print_tweet_string(tweetInfo, is_detailed=True)

    if (mode != "f"):
        looking = True
        while looking:
            looking = show_tweet_options(tweetInfo)