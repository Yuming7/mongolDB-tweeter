from getpass import getpass
import sqlite3, sys
import dashboard
from tweet import set_file
from user import set_file1
from search import set_file2
from dashboard_follows import set_file3



# Change from global variable to whatever we grabbed from main
file = None

# class holds username and password
class Session:
    def __init__(self,usr,pwd):
        self.usr = int(usr)
        self.pwd = pwd
    
    def getPwd(self):
        return self.pwd

    def getUsr(self):
        return self.usr

    def changeUsr(self, newUsr):
        self.usr = newUsr

    def changePwd(self, newPwd):
        self.pwd = newPwd

def exit_screen():
    print("     [...Shutting Down....]")
    exit()

def register_check(option):
    if option == "name":
            while True:
                try: 
                    name = str(input("        Name: "))
                    break
                except len(name.strip()) > 0:
                    print("""   Username cannot be blank""")
            return name

# defined error
class inputError(Exception):
    pass


def register_screen():
    print("""
    ________________________________________
    NEW USER REGISTRATION
    ++++++++++++++++++++++++++++++++++++++++
    """)
    # Need to add a way to check for valid inputs
    # Use a try and except inside a while loop for this
    # https://stackoverflow.com/questions/71616352/valueerror-exception-handling-in-a-while-loop-repeat-only-wrong-input

    while(True):
        try:
            #userName = register_check("name") #Should not be blank
            userName = str(input("        Name: "))
            if(len(userName.strip()) <= 0):
                raise inputError

        except inputError:
            print("Name should not be blank")
            
        else: 
            break
    while(True):
        try:
            userEmail = input("        Email: ") #should have '@' and end in .com|.net|.ca|.org|.edu
            if(len(userEmail.strip())<=0):
                raise inputError
        except inputError:
            print("Email should not be blank")
        else: 
            break
    while(True):
        try:
            userCity = input("        City: ") #should be at least 1 char long
            if(len(userCity.strip())<=0):
                raise inputError
        except inputError:
            print("City should not be blank")
            
        else: 
            break
    while(True):
            
        try:
            userTime = str(input("        Timezone: ")) #should be an int, no floats
            if(len(userTime.strip())<=0):
                raise inputError
            userTime = int(userTime)
        except inputError:
            print ("Timezone should not be blank")
        except:
            print("Timezone should be a float")
        else: 
            break

    userID = generate_usr()

    while(True):

        try:
            userPwd = getpass("        Password: ") #should be 6 - 20 char long
            if(len(userPwd.strip())>20 or len(userPwd.strip())<6):
                raise inputError("Password should be 6 - 20 char long")
        except inputError:
            print("Password should be 6 - 20 char long")
        else: 
            break

    

    
    '''
    userName = register_check("name") #Should not be blank
    userEmail = input("        Email: ") #should have '@' and end in .com|.net|.ca|.org|.edu
    userCity = input("        City: ") #should be at least 1 char long
    userTime = int(input("        Timezone: ")) #should be an int, no floats
    userID = int(str(ord(userName[0])) + str(ord(userEmail[0])) + str(ord(userCity[0])) + str(userTime))
    userPwd = getpass("        Password: ") #should be 6 - 20 char long
    '''

    # ADD PART THAT CHECKS IF USERID EXISTS

    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("""INSERT INTO users VALUES ('%d', '%s', '%s','%s','%s', %d)""" 
         % (userID, userPwd, userName, userEmail, userCity, userTime))
    conn.commit()
    c.close()

    newSession = Session(userID, userPwd)
    dashboard.home(newSession,file)

def login_screen():
    username = input("""
    ________________________________________
    LOGIN SCREEN
    ++++++++++++++++++++++++++++++++++++++++
                     
        Username: """)
    password = getpass("        Password: ")
    
    #Checks if user exists
    conn = sqlite3.connect(file)
    c=conn.cursor()

    user = c.execute("""SELECT * FROM users WHERE usr = '%s' AND pwd = '%s'"""
        % (username, password)).fetchone()

    if user:
        print("""
        Login Successful!
        """)
    else:
        print("""
        !!!
        Looks like you're not registered.
        Check your username and password.
        """)
        starting_screen(file)

    newSession = Session(username, password)
    dashboard.home(newSession,file)



def starting_screen(db):
    global file
    file = db
    # User options to Login, Register, or Exit
    set_file(file)
    set_file1(file)
    set_file2(file)
    set_file3(file)

    startingScreenMessage = """
    ________________________________________
    STARTING SCREEN
    ++++++++++++++++++++++++++++++++++++++++
    
    Select from the following:
        1.LOGIN    2.REGISTER    3.EXIT

        """
    choosing = True

    while choosing:
        startingChoice = str(input(startingScreenMessage))
        if startingChoice == "1":
            login_screen()
            choosing = False
        elif startingChoice == "2":
            register_screen()
            choosing = False
        elif startingChoice == "3":
            exit_screen()
        else:
            print(
    """
    !!!
    That is not a valid option. 
    Type the number of the option you wish to select.""")

def generate_usr() -> int:
    conn = sqlite3.connect(file)
    c=conn.cursor()

    c.execute("SELECT usr FROM users ORDER BY usr DESC;")
    usr = c.fetchone()[0]
    usr +=1
    print("Your user id is:",usr)
    c.close()
    return usr

# def main():
#     starting_screen()

# if __name__=="__main__":
#     main()


