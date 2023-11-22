import sqlite3, sys
import follow2, dashboard, search
file = None
conn = None
c = None
flwee = None

def set_file3(filename) -> None:
    global file, c, conn
    file = filename
    conn = sqlite3.connect(file)
    c = conn.cursor()

def follower_option():
    option = str(input(
    """
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    OPTIONS:
        1. Follower Info
        2. Follow Back 
                
        (H) Go back to feed
    ____________________________________________________________
    What would you like to do?  """))

    if option == "1":
        flwer = int(input("       Follower Username: "))
        followerList = follow2.get_my_followers(flwee)

        if flwer in followerList:
            follower_info(flwer)
        return True
    elif option == "2":
        flwer = int(input("        Followback Username: "))
        follow2.follow(flwee, flwer)
        print("        You have followed %d" % (flwer))
    elif option.upper() == "H":
        print(
    """[Returning to Dashboard]""")
        return False


def follower_info(flwer):
    c.execute("SELECET * FROM users WHERE users.usr = %d" % (flwer))
    user = c.fetchone()
    search.print_user_string(user,is_detailed=True)

def follower_menu(usr):
    global flwee
    flwee = usr
    follow2.display_followees((flwee,))
    looking = True

    while looking:
        looking = follower_option()
    