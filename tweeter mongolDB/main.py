import sqlite3, sys, session
#import  dashboard,dashboard_follows,follow,search, session, tweet, user

def main():
    # Grabs database name from command line argument
    if len(sys.argv) == 1:
        db = input("Enter your database name: ")
    else:
        db = sys.argv[1]

    # Adds '.db' extension if not available
    if db[len(db)-3:] != '.db':
        db += '.db'

    session.starting_screen(db)
    
if __name__=="__main__":
    main()
