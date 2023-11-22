import datetime
import sqlite3
import textwrap

file = None
conn = None
c = None


def set_file(filename) -> None:
    global file, c, conn
    file = filename
    conn = sqlite3.connect(file)
    c = conn.cursor()

def print_tweet_string(tweet: tuple, is_replyed_to: bool = False, is_detailed: bool = False, is_retweet: bool = False) -> None: 
    """
    format_tweet_string(tweet: tuple, is_replyed_to: bool = False, is_detailed: bool = False) -> None

    Prints a tweet (tid,writer,tdate,text,replyto) in the following format:

    ------------------------------------------------------------
    user_name   @user_id

    text text text text text text text text text text text text
    text text text text text text text text text text text text
    text text text text text text text text text text text text
    text text text text text text text text text text text text 

    retweets: no_rt   replies: no_rep                tweet_date 
    
    (last line only if is_detailed = True)

    Or in the case of a reply:

    ------------------------------------------------------------
    replying to: 
      user_name   @user_id

      |  text text text text text text text text text text text
      |  text text text text text text text text text text text
      |  text text text text text text text text text text text
      |  text text text text text text text text text text text
      |
      |
    replyer_name   @replyer_id

    text text text text text text text text text text text text 
    text text text text text text text text text text text text 
    text text text text text text text text text text text text 
    text text text text text text text text text text text text 

    retweets: no_rt   replies: no_rep                tweet_date 
    
    (last line only if is_detailed = True)
    """
    # conn = sqlite3.connect(FILENAME)
    # c=conn.cursor()
    tid,writer,tdate,text,replyto = tweet

    if is_replyed_to == False:
        print("\n"+60*"-"+"\n")
    if replyto != None:
        c.execute("SELECT * FROM tweets WHERE tid = %d;"%(replyto))
        replyed_to = c.fetchone()
        print_tweet_string(replyed_to, True)
    
    c.execute("SELECT name FROM users WHERE usr = %d;"%(writer))
    name = c.fetchone()[0]
    if is_replyed_to == False:
        # if is_retweet == True:
        #     print("retweeted: \n")
        print(name+"   @"+str(writer)+"\n")
        print(textwrap.fill(text,60, drop_whitespace=False))
        c.execute("SELECT term FROM mentions WHERE tid=%d;"%(tid))
        query=c.fetchall()
        if query != []:
            hashtags=[]
            for hashtag in query:
                term=hashtag[0]
                hashtags.append(term)
            hashtags=" #".join(hashtags)
            if hashtags != []:
                print("\n")
                print(textwrap.fill(hashtags,60, initial_indent = "#",drop_whitespace=False)) 
        if is_detailed == True:
            c.execute("SELECT count (*) FROM retweets WHERE tid=%d;"%(tid))
            no_retweets = c.fetchone()[0]
            c.execute("SELECT count (*) FROM tweets WHERE replyto=%d;"%(tid))
            no_replies = c.fetchone()[0]
            print(f"\nretweets: {no_retweets:<5}   replies: {no_replies:<5}{tdate:>27}\n")
        else:
            print(f"\n{tdate:<60}\n")
    else:
        print("replying to: \n  ")
        print(name+"   @"+str(writer)+"\n")
        print(textwrap.fill(text,60,initial_indent="  |  ",subsequent_indent="  |  ", drop_whitespace=False))
        print("  |\n  |")
    #c.close()
    
def display_tweets(tweets: list, quantity: int=5) -> list:
    """
    display_tweets(tweets: list[tuple], quantity: int) -> list

    Displays tweets (tid,writer,tdate,text,replyto) at 
    specified increment (quantity) and returns a list of tuples 
    of the displayed tweets so they can be referenced in replies 
    and retweets. First tweet displayed is index 1 in the list.
    """
    show_more = True
    index = 0
    displayed_tweets = [0]
    
    while show_more == True:
        for i in range(quantity):
            if i+index == len(tweets):
                print("")
                print(" End of Tweets ".center(60,"-")+"\n")
                show_more = False 
                break   
            else:
                tweet = tweets[i+index]
                displayed_tweets.append(tweet)
                print_tweet_string(tweet)
                i+=1
        if show_more == True:
            show_more = input("\nShow More?(y/n) ")
            while show_more.lower() not in ["y","n"]:
                show_more = input("Invalid Input. Show More?(y/n) ")
            if show_more.lower() == "n":
                show_more = False
            else:
                show_more=True
                index+=quantity
    return displayed_tweets

def compose_tweet(usr:int, replyto: int = None) -> bool:
    """
    compose_tweet(usr:int, replyto: int = None) -> bool

    replyto: tid

    returns True if tweet was sent, False if tweet was aborted.
    """
    # conn = sqlite3.connect(FILENAME)
    # c=conn.cursor()

    text = input("\nWhat's happening?\n\n")
    send_tweet = input("Send Tweet?(y/n) ")

    while send_tweet.lower() not in ["y","n"]:
        send_tweet = input("Invalid Input. Send Tweet?(y/n) ")
    if send_tweet.lower() == "n":
        print("Tweet Aborted.\n")
        c.close()
        return False

    tid = generate_tid()
    tdate = datetime.datetime.now()

    hashtags = input("Hashtags: ") 
    hashtags = parse_hashtags(hashtags)

    if hashtags != [""]:
        for item in hashtags:
            c.execute("INSERT OR IGNORE INTO hashtags (term) VALUES ('%s');"%(item))
            conn.commit()
            c.execute("INSERT INTO mentions (tid,term) VALUES (%d,'%s');"%(tid,item))
            conn.commit()
    if replyto == None:
        c.execute("UPDATE tweets SET writer=%d,tdate='%s',text='%s' WHERE tid=%d"%(usr,tdate,text,tid))
        conn.commit()
    else:
        c.execute("UPDATE tweets SET writer=%d,tdate='%s',text='%s',replyto='%s' WHERE tid=%d"%(usr,tdate,text,replyto,tid))
        conn.commit()
        print("Tweet Sent.")
    #c.close()

def parse_hashtags(text:str) -> list:
    """
    parse_hashtags(text:str) -> list

    example input: "#Edmonton #yeg #WINTER"
    example output: ["edmonton","yeg","winter"]
    """
    text=text[1:]
    terms = text.split("#")
    for i in range(len(terms)):
        terms[i]=terms[i].lower()

    return terms

def generate_tid() -> int:
    # conn = sqlite3.connect(FILENAME)
    # c=conn.cursor()

    c.execute("SELECT tid FROM tweets ORDER BY tid DESC;")
    tid = c.fetchone()[0]
    tid +=1
    c.execute("INSERT INTO tweets (tid) VALUES (%d);"%(tid))
    conn.commit()
    #c.close()
    return tid

# def retweet(usr: int,tweet: tuple) -> None:
#     """
#     retweet(usr: int,tweet: tuple) -> None
#     """
#     conn = sqlite3.connect(FILENAME)
#     c=conn.cursor()
#     tid=tweet[0]
#     rdate=datetime.datetime.now()

#     c.execute("INSERT INTO retweets (usr,tid,rdate) VALUES (%d,%d,'%s');"%(usr,tid,rdate))
#     conn.commit()
#     c.close()
#     print("Retweet sent.")

def main():
    # conn = sqlite3.connect(FILENAME)
    # c=conn.cursor()
    c.execute("SELECT * FROM tweets WHERE writer=%d"%(20))
    tweet = c.fetchone()
    #compose_tweet(10, replyto=None, retweet=tweet)


#main()
