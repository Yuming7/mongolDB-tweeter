import sqlite3
import tweet,user
from show_tweet import show_tweet_info
from show_user import show_user_info

file = None
conn = None
c = None


def set_file2(filename) -> None:
    global file, c, conn
    file = filename
    conn = sqlite3.connect(file)
    c = conn.cursor()

# search for tweets based on the key words inputted
def search_tweet(key):

    # strip then splits the input into list
    key = key.rstrip()
    key = list(key.split(" "))
    print("key words:",key)

    hash = []
    keywords = []
    # splits the hastags and regular keywords into 2 different lists
    for entry in key:
        if(entry[0]=='#' and len(entry)>0):
            # removes the # before adding it to the list
            hash.append(entry[1:])
        else:
            keywords.append(entry)
    # query statements
    query_key = "SELECT t.* FROM tweets t WHERE "
    query_hash = "SELECT t.* FROM tweets t LEFT JOIN mentions m ON t.tid = m.tid  WHERE "

    condition_key = []
    condition_hash = []
    # for every element in each of the list, add the appropriate conditions
    for element in keywords:
        condition_key.append("t.text LIKE ?")
    for element in hash:
        condition_hash.append("(m.term LIKE ?)")

    # joins the conditions with OR
    query_key += " OR ".join(condition_key)
    query_hash += " OR ".join(condition_hash)
    # gets the parameters for each query
    param_key = [f"%{entry}%" for entry in keywords]
    param_hash = [f"%{entry}%" for entry in hash]

    rows_key = []
    rows_hash = []
    # only executes the query if their list of keywords are not 0
    if(len(keywords)>0):
        c.execute(query_key, param_key)
        rows_key = c.fetchall()
    if(len(hash)>0):
        c.execute(query_hash, param_hash)
        rows_hash = c.fetchall()

    # adds the rows together
    rows = rows_key+ rows_hash
    # sorts the rows based off of the third column(tdate) in descending order
    rows.sort(key=lambda x: x[2], reverse=True)
    # calls the display function
    select = display(rows,'t')

    #tweet.display_tweets(rows)

    if(select != None):
        pass

 
# search for users whose name matches the keyword and/or city
def search_user(key):

    # strip then splits the input into list
    key = key.rstrip()
    key = list(key.split(" "))
    print("key words:",key)

    # declares variables for the query
    query_name = "SELECT * FROM users u WHERE "
    query_city = "SELECT * FROM users u WHERE "
    condition_name = []
    condition_city = []
    param_name = []
    param_city = []

    # search users name who match the keyword
    for entry in key:
        condition_name.append("u.name LIKE ?")

    # search users city who match the keyword but not name
    for entry in key:
        condition_city.append("(u.name NOT LIKE ? AND u.city LIKE ?)")
        
    # joins the conditions using OR and adds them to the query
    query_name += " OR ".join(condition_name)
    query_city += " OR ".join(condition_city)
    # order by length of their respective query
    query_name += " ORDER BY LENGTH(u.name)"
    query_city += " ORDER BY LENGTH(u.city)"
    # writes parameters to fill the ? in the query
    param_name = [f"%{entry}%" for entry in key]
    param_city = [f"%{entry}%" for entry in key for i in range(2)]

    # executes the queries then add the results together
    c.execute(query_name,param_name)
    rows_name = c.fetchall()

    c.execute(query_city,param_city)
    rows_city = c.fetchall()

    rows = rows_name + rows_city

    # calls the display function
    

    select = display(rows,'u')
    return select

# displays 5 elements at a time, lets the user select one or quit
def display(alist,mode, n = 5):
    # removes duplicates by changing the list to keys then back to list
    alist = list(dict.fromkeys(alist))
    if(len(alist)==0):
        print(f"{' No results ':-^60}")
        return None
    
    pos = 0
    # loops through the list
    while pos<len(alist):
        count = 0
        # prints out n elements of the list at a time
        for i in range(pos,min(pos+n,len(alist))):    # min allows accessing of list of pages of less than size 5
            count += 1
            #print(str(count) + ":",alist[i])
            print(60*'-')
            if(mode == 't'):
                print(f'{str(count):^60}',end='')
                tweet.print_tweet_string(alist[i])
            elif(mode == 'u'):
                print(f'{str(count):^60}')
                print_user_string(alist[i])
            pos +=1
        # error checking for input
        run = True
        while(run):
            user_input = input(
    """ 
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    OPTIONS:
        Next Page - press any key
        See Detail -  select a number

        (H) Go back to feed
    ____________________________________________________________
    What would you like to do?   
    """)
            # if the user inputs a number, checks if it is valid
            if(user_input.isdigit()):
                if(int(user_input)>count or int(user_input)<=0):
                    print("    !!!\ninvalid input")
                    continue
            run = False
        # breaks the loop if the user wants to quit
        if(user_input.lower()=="h"):
            break
        # prints out the selected user and breaks the loop
        elif(user_input.isdigit()):
            select = alist[pos-count+int(user_input)-1]
            # find out if tweet or user
            # if tweet -> run show_tweet (tid, db)
            # if user -> run show_user (usr, db)
            # print( ="        selected",select)
            if(mode == "t"):
                show_tweet_info(select)
            elif(mode == "u"):
                show_user_info(select[0],file)
            return select

    return None

# connect to database
def connect(path):
    global conn, c
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(' PRAGMA foreign_keys=ON; ')
    conn.commit()
    return

def print_user_string(user: tuple, is_detailed: bool = False) -> None: 
    """
    print_user_string(user: tuple, is_detailed: bool = False) -> list (displayed tweets)

    Prints a user string (usr,pwd, name,email,city,timezone) in the following format:

    is_detailed = False:
    ------------------------------------------------------------
    name                                                    city
    
    is_detailed = True:
    ------------------------------------------------------------
    name                                                    city
    @user_id

    no_posts posts    no_flwer following    no_flwee followers
    ------------------------------------------------------------
    print_tweet_string(tweet1)
    ------------------------------------------------------------
    print_tweet_string(tweet2)
    ------------------------------------------------------------
    print_tweet_string(tweet3)

    """
    # conn = sqlite3.connect(FILENAME)
    # c=conn.cursor()
    (usr,pwd,name,email,city,timezone) = user
    print(60*"-")
    print(f"{name:<40}{city:>20}")
    if is_detailed == True:
        print(f"@{usr}\n")
        c.execute("SELECT COUNT(*) FROM tweets WHERE writer=%d;"%(usr))
        posts=c.fetchone()[0]
        #print(f"{posts} posts\n\n")
        c.execute("SELECT COUNT(*) FROM follows WHERE flwer=%d;"%(usr))
        following=c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM follows WHERE flwee=%d;"%(usr))
        followers=c.fetchone()[0]
        print(f"\n{posts} posts    {following} following    {followers} followers")
        c.execute("SELECT * FROM tweets WHERE writer=%d ORDER BY tdate DESC;"%(usr))
        tweets = c.fetchall()
        display(tweets,"t",3)
        
def main():
    # conn
    global conn, c

    #path = "./search_test1.db"
    path = "./test.db"
    connect(path)

    # temporary input
    a = input("enter tweet key words: ")
    search_tweet(a)

    a = input("enter user keyword: ")
    search_user(a)
    conn.close()

#if __name__=="__main__":
#    main()
