# mongolDB-tweeter


Project Description: Twitter-like Social Media Platform Using MongoDB

Introduction:
The project aims to create a Twitter-like social media platform, utilizing MongoDB as the backend database to store and manage user information, tweets, followers, and other relevant data. The system is designed to provide a seamless experience for both registered and unregistered users, offering functionalities such as user authentication, tweet management, user search, and more.

Database Specification:
The system uses the following relational schema:

users(usr, pwd, name, email, city, timezone)
follows(flwer, flwee, start_date)
tweets(tid, writer, tdate, text, replyto)
hashtags(term);
mentions(tid, term)
retweets(usr, tid, rdate)
lists(lname, owner)
includes(lname, member)
Login Screen:
The login screen provides options for registered and unregistered users. Registered users can log in using a valid user id (usr) and password (pwd). After login, the system displays the latest tweets or retweets from followed users, with an option to view more. Unregistered users can sign up by providing necessary details. Upon successful login or signup, users can perform subsequent operations.

System Functionalities:
After successful login, users can perform the following tasks:

Search for Tweets:

Users can enter keywords, and the system retrieves tweets matching the keywords.
Tweets are ordered by date, with an option to view more.
Users can view tweet statistics, compose replies, or retweet.
Search for Users:

Users can enter a keyword, and the system retrieves matching users.
Results are sorted by name length and city length, with an option to view more.
Users can view user information, follow, or view more tweets.
Compose a Tweet:

Users can compose tweets with hashtags.
Hashtag information is stored in the mentions and hashtags tables.
List Followers:

Users can list all followers, view follower information, and follow them or view more tweets.
Logout:

Users can log out of the system.
String Matching:

Passwords are case-sensitive, while other string matches are case-insensitive.
The system supports case-insensitive searches for tweets and users.
Security Measures:

SQL injection attacks are countered to ensure the security of the system.
Passwords are not visible during typing for added security.
Error Checking:

The system incorporates basic error checking to handle incorrect data entry.
Users are provided with a robust experience even when mistakes are made.
This Twitter-like social media platform built on MongoDB offers a secure, user-friendly, and feature-rich environment for users to engage, share tweets, and connect with others.
