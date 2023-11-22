import sqlite3, sys
import search, follow2

usr = None
def set_user(usrID):
    global usr
    usr=usrID


def show_user_options(userInfo):
    option = str(input("""
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    OPTIONS:
        1. Follow        
        2. More Tweets 

        (H) Go back to feed
    ____________________________________________________________
    What would you like to do?  """))

    if option == "1":
        #print("placeholder: follow user")
        follow2.follow(usr,userInfo[0])
        return True
    elif option == "2":
        print("placeholder: Show more tweets from user")

    elif option.upper() == "H":
        print(
    """[Returning to Dashboard]""")
        return False
    
def show_user_info(userID, file):
    conn = sqlite3.connect(file)
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE users.usr = %d" % (userID))
    userInfo = c.fetchone()

    search.print_user_string(userInfo, is_detailed=True)

    looking = True
    while looking:
        looking = show_user_options(userInfo)
    
