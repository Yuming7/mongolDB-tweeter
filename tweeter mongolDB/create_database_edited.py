import sqlite3

conn = sqlite3.connect('test.db')

c=conn.cursor()

c.executescript("""   DROP TABLE if EXISTS includes;
                DROP TABLE if EXISTS lists;
                DROP TABLE if EXISTS retweets;
                DROP TABLE if EXISTS mentions;
                DROP TABLE if EXISTS hashtags;
                DROP TABLE if EXISTS tweets;
                DROP TABLE if EXISTS follows;
                DROP TABLE if EXISTS users;

                CREATE TABLE users (
                usr         int,
                pwd	      text,
                name        text,
                email       text,
                city        text,
                timezone    float,
                PRIMARY KEY (usr)
                );
                CREATE TABLE follows (
                flwer       int,
                flwee       int,
                start_date  date,
                PRIMARY KEY (flwer,flwee),
                FOREIGN KEY (flwer) REFERENCES users,
                FOREIGN KEY (flwee) REFERENCES users
                );
                CREATE TABLE tweets (
                tid	      int,
                writer      int,
                tdate       date,
                text        text,
                replyto     int,
                PRIMARY KEY (tid),
                FOREIGN KEY (writer) REFERENCES users,
                FOREIGN KEY (replyto) REFERENCES tweets
                );
                CREATE TABLE hashtags (
                term        text,
                PRIMARY KEY (term)
                );
                CREATE TABLE mentions (
                tid         int,
                term        text,
                PRIMARY KEY (tid,term),
                FOREIGN KEY (tid) REFERENCES tweets,
                FOREIGN KEY (term) REFERENCES hashtags
                );
                CREATE TABLE retweets (
                usr         int,
                tid         int,
                rdate       date,
                PRIMARY KEY (usr,tid),
                FOREIGN KEY (usr) REFERENCES users,
                FOREIGN KEY (tid) REFERENCES tweets
                );
                CREATE TABLE lists (
                lname        text,
                owner        int,
                PRIMARY KEY (lname),
                FOREIGN KEY (owner) REFERENCES users
                );
                CREATE TABLE includes (
                lname       text,
                member      int,
                PRIMARY KEY (lname,member),
                FOREIGN KEY (lname) REFERENCES lists,
                FOREIGN KEY (member) REFERENCES users
                ); """)

conn.commit()

insert_tweets = '''
                    INSERT INTO tweets(tid,writer,tdate,text,replyto) VALUES
                        (1,10,'2023-01-01','GOGOGOGO',NULL),
                        (2,10,'2019-01-01','#good',NULL),
                        (3,10,'2020-01-01','same',NULL),
                        (4,10,'2020-01-02','die',NULL),
                        (5,20,'2023-04-04','testtest 123 #test',NULL),
                        (6,10,'2020-09-09','hello',5),
                        (7,10,'2023-02-01','database',3),
                        (8,50,'2020-10-10','same database hello #good',NULL),
                        (9,20,'2019-12-12','asdf',NULL),
                        (10,10,'2019-12-11','qwer',NULL);


'''

insert_mentions = '''
                    INSERT INTO mentions(tid,term) VALUES
                        (3,'wow'),
                        (1,'wow'),
                        (5,'data');

'''
c.execute(insert_tweets)
c.execute(insert_mentions)
# user
c.execute("""
INSERT INTO users(usr,pwd, name,email,city,timezone) VALUES
  (10,'1234','John Doe','john@email.com','Edmonton',7.0),
  (20,'hotdog','Jones Doe','jones@email.ca','Boston',7.0),
  (30,'qwerty','Alice Johnson','alice@email.com','Edmonton',5.0),
  (40,'hockey','Joe Doe','joe@email.com','Doe Town',0.0),
  (50,'passowrd','Allan Smith','allan@emal.com','Edmonton',3.0),
  (60,'1423','Sarah Doe','sarah@email.com','New York',7.0),
  (70,'asdf','Ed Wong','ed@email.com','New York',7.0);
              

""")
# follows
c.execute("""
INSERT INTO follows(flwer,flwee,start_date) VALUES
          (10,20,'2020-10-10'),
          (10,30,'2020-10-10'),
          (10,40,'2020-10-10'),
          (10,70,'2020-10-10'),
          (20,10,'2020-10-10'),
          (20,30,'2020-10-10'),
          (10,50,'2020-10-10'),
          (30,50,'2020-10-10'),
          (30,10,'2020-10-10'),
          (40,10,'2020-10-10'),
          (50,10,'2020-10-10'),
          (50,20,'2020-10-10'),
          (60,10,'2020-10-10'),
          (60,50,'2020-10-10'),
          (70,10,'2020-10-10'),
          (70,40,'2020-10-10'),
          (70,60,'2020-10-10');
  
""")
# retweets
c.execute("""
INSERT INTO retweets(usr,tid,rdate) VALUES
          (70,1,'2023-04-04'),
          (70,5,'2023-04-04'),
          (60,4,'2023-04-04'),
          (30,1,'2023-04-04'),
          (10,9,'2023-04-04'),
          (40,5,'2023-04-04');
""")
c.execute("""
INSERT INTO hashtags(term) VALUES
          ('wow'),
          ('data');

""")
conn.commit()
