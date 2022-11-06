
import sys
sys.path.append(r"C:\Users\huseen marcelo\Desktop\Informatique\1_Visual\2_Project\Flask\2021\6_cs50\3_improvement\sqlite_class\finance")


from helpers import db


"""Classes that have methods() to create,update,insert,... to database"""
###############################################################################################################################################

#   TABLE users( id,  username,  hash,   cash )
class User():

    def __repr__(self):
        return '<User>'

    @staticmethod                                         
    def add(username, hash_psw):
        
        # ############################# Add user to database ############################# #
        
        # Return [] of id & cash of inserted user
        user_id = db.execute("INSERT INTO users (username,hash) VALUES(?,?)", (username, hash_psw)).lastrowid
        db.commit()

        #  return ====> tuple ===> (1000.00)
        startCash = db.execute("SELECT cash FROM users WHERE id = ?", (user_id,)).fetchone()[0]

        id_cash = [user_id, startCash]
        return id_cash
        
    # --------------------------------------------------------------------------------

    @staticmethod                                         
    def update_cash(user_id, profit):

        db.execute("UPDATE users SET (cash) = ? WHERE (id) = ?", (profit, user_id))
        db.commit()

    # 
    @staticmethod                                         
    def get_profit(user_id):
        
        # ########### Add total of (all purchases) with (currentCash from cash) ====> to se the difference (win or lose) ############# #

        profit = db.execute(
            "SELECT (SELECT SUM(total) FROM purchase) + (SELECT currentCash FROM cash WHERE user_id = ?) as result", (user_id,)).fetchone()[0]
        return profit


###############################################################################################################################################

#  TABLE blog( id,  user_id,  title,   author,  content,  date,  img  ) 
class Blog():

    def __repr__(self) :
        return f"<Blog user_id={self.user_id}>"

    # --------------------------------------------------------------------------------

    @staticmethod                                         
    def add(user_id, title, author, content, date, img):
        
        db.execute(
            "INSERT INTO blog (user_id, title, author, content, date, img) VALUES (?,?,?,?,?,?)", (user_id, title, author, content, date, img))
        db.commit() 
        
    @staticmethod                                        
    def delete(blogId):
        db.execute("DELETE FROM blog WHERE id = ?", (blogId,) )
        db.commit() 



###############################################################################################################################################

# TABLE note( id,  user_id,  data )
class Note():

    def __repr__(self) :
        return f"<Note>"

    # --------------------------------------------------------------------------------

    @staticmethod                                     
    def add(user_id, note):
        db.execute("INSERT INTO note (user_id, data) VALUES (?,?)", (user_id, note))
        db.commit()
        

    @staticmethod                                          
    def delete(note_id):
        db.execute("DELETE FROM note WHERE id = ?", (note_id,))
        db.commit()


###############################################################################################################################################


# TABLE purchase( user_id,  symbol,  name,  shares,   price,   total )

class Purchase():
    
    def __repr__(self) :
        return f"<Purchase>"
    
    # --------------------------------------------------------------------------------

    @staticmethod                                         
    def add(user_id, symbol, name, shares, latestPrice, totalBought):

        db.execute( "INSERT INTO purchase (user_id, symbol, name, shares, price,total) VALUES (?,?,?,?,?,?)", (user_id, symbol, name, shares, latestPrice, totalBought))
        db.commit()


    @staticmethod                                          
    def update_buy(user_id, symbol, shares, totalBought, latestPrice):

        #  ############### Update ====> add to (shares) & (total) ====> set (price) = latestPrice ################## 

        db.execute("UPDATE purchase SET (shares, price, total) = (shares + ?, ?, total + ?) WHERE (user_id, symbol) = (?,?)", (shares, latestPrice, totalBought, user_id, symbol))
        db.commit()  

    # --------------------------------------------------------------------------------

    @staticmethod                                       
    def update_sell(user_id, symbol, demand_share, old_price):
        
        #  ############### Update ====> Substract from (shares) & (total)  ##################   
        
        db.execute("UPDATE purchase SET (shares, total) = (shares - ?, total - ?) WHERE (user_id, symbol) = (?,?) ", (demand_share, old_price, user_id, symbol))
        db.commit()
        

    @staticmethod                                         
    def delete_zero_shares():
        
        db.execute("DELETE FROM purchase WHERE shares = 0")
        db.commit()

###############################################################################################################################################

# TABLE cash( user_id,  currentCash )
class Cash:

    def __repr__(self) :
        return f"<Cash>"

    @staticmethod
    def set_Current_Cash(user_id, startCash):

        #   ############### Insert ====> once the user register  ##################   

        db.execute("INSERT INTO cash (user_id, currentCash) VALUES (?,?)", (user_id, startCash))
        db.commit()
        
        
    @staticmethod
    def get_Current_Cash(user_id):

        current_Cash = db.execute("SELECT currentCash FROM cash WHERE (user_id) = ?", (user_id,)).fetchone()[0]
        return current_Cash
        

    # --------------------------------------------------------------------------------

    @staticmethod
    def substract_current_cash(user_id, totalBought):

        #   ############### UPDATE ====> when user buy a stock  ##################   
    
        db.execute("UPDATE cash SET (currentCash) = (currentCash - ?) WHERE user_id = (?) ", (totalBought, user_id,))
        db.commit()

    @staticmethod                                   
    def add_current_cash(user_id, new_price):

        #   ############### UPDATE ====> when user sell a stock  ##################   

        db.execute("UPDATE cash SET currentCash = (currentCash + ?) WHERE (user_id) = (?)", (new_price, user_id))
        db.commit()

###############################################################################################################################################

# TABLE transactions( user_id,  symbol,  shares,  price,  transacted )
class Transactions():
    
    def __repr__(self) :
        return f"<Transactions>"

    # --------------------------------------------------------------------------------

    @staticmethod                                        
    def add(user_id, symbol, shares, latestPrice, transacted):
        
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, transacted) VALUES (?,?,?,?,?)",
                (user_id, symbol, shares, latestPrice, transacted))
        db.commit()


    @staticmethod                                       
    def get_last_price(user_id, symbol):

        #   ############### when SOLD of stock ===> last bought price so we can substract from purchase total   ##################   

        boughtPrice = db.execute(
            "SELECT price FROM transactions WHERE (user_id, symbol) = (?,?) AND shares > 0 ORDER BY(transacted) DESC LIMIT 1 ", (user_id, symbol)).fetchone()[0]

        return boughtPrice
    


###############################################################################################################################################



