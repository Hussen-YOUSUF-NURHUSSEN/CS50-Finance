

import sys
sys.path.append(r"C:\Users\huseen marcelo\Desktop\Informatique\1_Visual\2_Project\Flask\2021\6_cs50\3_improvement\sqlite_class\finance")

from helpers import db


""" Create the database by running this file """

""" TABLES =========>  users,  blog,  note,  purchase,  cash,  transactions   """
######################################################################################################################################
######################################################################################################################################
############################################################## Database ##############################################################
######################################################################################################################################
######################################################################################################################################

cr = db.cursor()


# users
cr.execute("""CREATE TABLE IF NOT EXISTS 
                    users(
                            id       INTEGER,
                            username TEXT NOT NULL,
                            hash     TEXT NOT NULL,
                            cash     NUMERIC NOT NULL DEFAULT 10000.00,

                            PRIMARY KEY(id) 
                        )
""")

# blog
cr.execute("""CREATE TABLE IF NOT EXISTS
                    blog(
                            id       INTEGER,
                            user_id  INTEGER,

                            title    TEXT,
                            author   TEXT,
                            content  TEXT,
                            date     TEXT,
                            img      TEXT,

                            PRIMARY KEY (id),
                            FOREIGN KEY(user_id) REFERENCES users(id)
                        )
""")

# note
cr.execute("""CREATE TABLE IF NOT EXISTS
                    note(
                            id       INTEGER,
                            user_id  INTEGER,
                            data VARCHAR(10000),

                            PRIMARY KEY (id),
                            FOREIGN KEY(user_id) REFERENCES users(id)
                        )
""")

# purchase
cr.execute("""CREATE TABLE IF NOT EXISTS
                purchase(

                            user_id  INTEGER,
                            name     TEXT NOT NULL,
                            
                            price    NUMERIC NOT NULL,
                            symbol   TEXT NOT NULL,
                            shares   INTEGER,
                            total    NUMERIC NOT NULL,

                            FOREIGN KEY(user_id) REFERENCES users(id)
                        )
""")

# cash
cr.execute("""CREATE TABLE IF NOT EXISTS
                    cash(
                            user_id     INTEGER,
                            currentCash NUMERIC,

                            FOREIGN KEY(user_id) REFERENCES users(id) 
                        )
""")

# transactions
cr.execute("""CREATE TABLE IF NOT EXISTS
                transactions(

                                user_id    INTEGER,
                                symbol     TEXT,
                                
                                shares     INTEGER,
                                price      NUMERIC NOT NULL,
                                transacted TEXT,
                                
                                FOREIGN KEY(user_id) REFERENCES users(id)
                            )
""")

