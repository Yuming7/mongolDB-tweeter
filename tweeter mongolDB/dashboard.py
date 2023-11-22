import sqlite3, sys
import session, follow,tweet, show_tweet, search
from dashboard_follows import follower_menu
from show_user import set_user


#Global Variables
DISPLAY = 5
page = 0
count = 1
conn, c, file, usr, tweet_feed = None, None, None, None, None

def userOption():
    print("\n")
    option = str(input(
    """
    What would you like to do? """))

    if option == "1":
        next_page()
        return True
    elif option == "2":
        previous_page()
        return True
    
    # Look at tweet info
    elif option == "3": 
        chosenTweet = int(input(
"""
Select tweet to look at:  
"""))
        if chosenTweet in range(1, len(tweet_feed)):
                show_tweet.show_tweet_info(tweet_feed[chosenTweet-1][1])
        else:
            print(
"""
That is not a valid tweet...
""")
        return True
    elif option == "4":
        tweet.compose_tweet(usr)
        #print("Post")
        return True
    elif option == "5":
        print(
"""

""")
        while(True):
            search_input = input("What would you like to search? 1 for tweet, 2 for user: ")
            if(search_input != '1' and search_input != '2'):
                continue
            break
        
        if(search_input == '1'):
            key = input("input tweet keywords: ")
            search.search_tweet(key)
        elif(search_input == '2'):
            key = input("input user keywords: ")
            search.search_user(key)
        return True


    # Look at followers    
    elif option == "6":      
        follower_menu(usr)
        return True
    
    elif (option == "Q") or (option == 'q') :
        print("""
    [...Logging out...]
    ____________________________________________________________""")
        return False
    else:
        print("""
    !!!
    That is not a valid option. 
    Type the number of the option you wish to select.
    """)
        return True
        
def display_tweets():
    pageStop = page*DISPLAY + DISPLAY
    global count, file
    show_tweet.set_db(file)

    if pageStop > len(tweet_feed):
        pageStop = len(tweet_feed)

    for tweet in range(page, pageStop):
        poster = tweet_feed[tweet][0]
        writer = tweet_feed[tweet][2]
        date = tweet_feed[tweet][3]
        text = tweet_feed[tweet][4]

        #Get names of users from database
        global conn, c
        conn = sqlite3.connect(file)
        c = conn.cursor()

        posterName = c.execute("SELECT name FROM users WHERE users.usr = %d;" % (poster)).fetchone()

        print("""
    ------------------------------------------------------------
                                %d""" % (count))
        
        #If tweet is a retweet
        if poster != writer:
            writerName = c.execute("SELECT name FROM users WHERE users.usr = %d;" % (writer)).fetchone()
            print(
    """
    ------------------------------------------------------------
    RETWEETED BY %s  @%d              
    """ % (posterName[0], poster))
        
        show_tweet.show_tweet_info(tweet_feed[tweet][1], "f")
        count += 1
    conn.close()
    
def previous_page():
    global page
    
    if (page - DISPLAY) < 0:
        print("""
        !!!
        This is the first page!
        """)
    else:
        page -= DISPLAY

        display_tweets()

# Goes to next five tweets to display
def next_page():
    global page

    if (page + DISPLAY) > len(tweet_feed):
        print("""
        !!!
        You've reached the end of your feed!
        """)
    else:
        page += DISPLAY

        display_tweets()
    
def feed():
    global conn, c, usr
    conn = sqlite3.connect(file)
    c = conn.cursor()

    #TODO POPULATE OTHER FILES SO OPTIONS ARE READY
    #Add in function to grab followers here
    follow.get_db(file)

    # Top of Feed
    print("""
    ____________________________________________________________
    DASHBOARD OF %s                                           
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++""" %(usr))


    # Union of Tweets from Following and Retweets from Following
    c.execute("""
    SELECT u2.usr, t.tid, t.writer, t.tdate AS date, t.text
    FROM tweets t, users u1, users u2, follows f
    WHERE u1.usr = %d AND u1.usr = f.flwer AND u2.usr = f.flwee
    AND u2.usr = t.writer
    
    UNION
    
    SELECT u2.usr, t.tid, t.writer, rt.rdate AS date, t.text
    FROM tweets t, retweets rt, users u1, users u2, follows f
    WHERE u1.usr = %d AND u1.usr = f.flwer AND u2.usr = f.flwee
    AND u2.usr = rt.usr and rt.tid = t.tid
              
    ORDER BY date DESC
    """ % (usr, usr))

    global tweet_feed
    tweet_feed = c.fetchall()

    if len(tweet_feed) == 0:
        print("""
        ...Feed is empty.
        """)
    else:
        display_tweets()

    conn.close()

def home(session_info, db):
    global file, usr
    set_user(usr)
    file = db
    usr = session_info.getUsr()
    show_tweet.set_user(usr)

    # Option menu
    online = True
    while online:
        # Print feed of tweets here
        feed()

        print("""
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    OPTIONS:
        1. Next Page    2. Previous Page    3. Look at Tweet
        4. Post         5. Search           6. Followers
              
        (Q) Log out
    ____________________________________________________________""")
        online = userOption()
    
    session.starting_screen(file)
    






    
