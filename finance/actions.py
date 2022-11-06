from flask import render_template, session, Blueprint, request, flash, redirect
from .helpers import login_required, lookup, db
from datetime import datetime
from finance.model.database import Cash, Purchase, Transactions, Note, Blog, User

"""  Routes in this blueprint  ===>   /buy    /sell  """

# Create blueprint
actions = Blueprint("actions", __name__)


@actions.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        # --------------------------------------------------------------------------------

        symbol = request.form.get("symbol")

        # applogy() if symbol don't exisit, or shares negative/fractional
        if not symbol:
            flash("Missing symbol", category='error')
            return redirect("/buy")

        # flash if symbol don't exisit, or shares negative/fractional
        quotes = lookup(symbol)
        if quotes == None:
            flash("Invalid symbol", category='error')
            return redirect("/buy")

        # --------------------------------------------------------------------------------

        shares = request.form.get("shares")

        try:
            shares = int(shares)
        except ValueError:
            flash("Invalid share", category='error')
            return redirect("/buy")

        if shares < 1:
            flash("Not positive number", category='error')
            return redirect("/buy")

        # --------------------------------------------------------------------------------

        # JSON response from quotes()
        latestPrice = quotes['price']
        symbol      = quotes['symbol']
        name        = quotes['name']

        user_id     = session["user_id"]
        totalBought = latestPrice * shares

        # Get current_Cash to see if user have enough money        
        get_cash = Cash.get_Current_Cash(user_id)
        
        current_Cash = get_cash - totalBought

        # --------------------------------------------------------------------------------

        if current_Cash >= 0:

            Cash.substract_current_cash(user_id, totalBought)
            
            # Create or Update a purchase
            row = db.execute("SELECT symbol FROM purchase WHERE (user_id, symbol) = (?,?)", (user_id, symbol,)).fetchall() 

            if len(row) == 0:
                # Create        
                Purchase.add(user_id, symbol, name, shares, latestPrice, totalBought)         
            else:
                # Update ====> add to (shares) & (total) ====> set (price) = latestPrice
                Purchase.update_buy(user_id, symbol, shares, totalBought, latestPrice) 
        else:
            flash("Can't afford", category='error')
            return redirect("/buy")

        # --------------------------------------------------------------------------------

        # Keep a record for /history
        now = datetime.now()
        transacted = now.strftime("%Y-%m-%d %H:%M:%S")

        Transactions.add(user_id, symbol, shares, latestPrice, transacted)

        flash("Bought!", category="success")
        return redirect("/")

    return render_template("buy.html")



@actions.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    SYMBOLS = []
    user_id = session["user_id"]

    # TABLE ======> purchase (user_id, symbol, name, shares, price, total)

    # Except list[] of tuples() with symbol
    purchases = db.execute("SELECT symbol FROM purchase WHERE (user_id) = ? ", (user_id,)).fetchall()

    # --------------------------------------------------------------------------------

    # Add the symbols that user have to a list []
    for purchase in purchases:
        SYMBOLS.append(purchase[0])

    # --------------------------------------------------------------------------------

    if request.method == 'POST':

        symbol = request.form.get("symbol")
        if not symbol:
            flash("Missing symbol", category='error')
            return redirect("/sell")

        if symbol not in SYMBOLS:
            flash("Symbol not owend", category='error')
            return redirect("/sell")

        # --------------------------------------------------------------------------------

        # Check if user have enough shares
        shares = db.execute("SELECT shares FROM purchase WHERE (user_id, symbol) = (?,?)", (user_id, symbol)).fetchone()[0]
        demand_share = request.form.get("shares")

        if not demand_share:
            flash("Missing share", category='error')
            return redirect("/sell")

        # --------------------------------------------------------------------------------

        try:
            demand_share = int(demand_share)
        except ValueError :
            flash("Invalid share", category='error')
            return redirect("/sell")


        if demand_share > shares:
            flash("Too many shares", category='error')
            return redirect("/sell")
        if demand_share < 0:
            flash("Not positive", category='error')
            return redirect("/sell")

        # --------------------------------------------------------------------------------

        # Get last price from transactions, so so we can substract from purchase total 
        boughtPrice = Transactions.get_last_price(user_id, symbol)

        old_price = demand_share * boughtPrice

        # SUBTRACT shares and total of the sold symbol
        Purchase.update_sell(user_id, symbol, demand_share, old_price)

        # --------------------------------------------------------------------------------

        # Request for latestPrice
        quotes = lookup(symbol)
        latestPrice = quotes['price']

        new_price = demand_share * latestPrice

        # Update the currentCash 
        Cash.add_current_cash(user_id, new_price)


        ##################################### win or lose based on stock latestPrice #####################################

        # Add total of (all purchases) + (currentCash from cash) ====> to se the difference (win or lose)
        profit = User.get_profit(user_id)

        print(f" (action.py) line 169 =====================================> {profit}")
        
        # Update the cash in user table
        User.update_cash(user_id, profit)

        # Delete purchases where shares = 0
        Purchase.delete_zero_shares()

        # --------------------------------------------------------------------------------
        
        # For ==> history.html
        now = datetime.now()
        transacted = now.strftime("%Y-%m-%d %H:%M:%S")

        Transactions.add(user_id, symbol, shares, latestPrice, transacted)   # maybe change "shares" to "demand_share"
        

        flash("Sold!", category="success")
        return redirect("/")

    return render_template("sell.html", symbols=SYMBOLS)









