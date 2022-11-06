from flask import render_template, session, Blueprint, request, flash, redirect
from .helpers import login_required, usd, lookup, db

"""  Three routes in 'views blueprint'  ===>   /    /history    /quote    """

# Create blueprint
views = Blueprint("views", __name__)


@views.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # TABLE ====> purchase (user_id, symbol, name, shares, price, total)

    # Return a list [] of tubles () of all purchases, template is going to iterate it to extract the data into a table
    purchases = db.execute("SELECT * FROM purchase WHERE (user_id) = (?)", (session["user_id"],)).fetchall()


    # Convert it to list[] because tuble are immutable - then format with usd()
    for i in range(len(purchases)) :
        purchases[i] = list(purchases[i])
        purchases[i][2] = usd(purchases[i][2])
        purchases[i][5] = usd(purchases[i][5])
    
    # The initial cash in users TABLE  ==> will vary if we sell
    startCash = db.execute("SELECT cash FROM users WHERE id = (?)", (session['user_id'],)).fetchone()[0]

    startCash = usd(startCash)

    # Dynamic cash to keep track of (purchases - startCash )
    current_Cash = db.execute("SELECT currentCash FROM cash WHERE (user_id) = (?)", (session["user_id"],)).fetchone()[0]
    current_Cash = usd(current_Cash)

    return render_template("index.html", purchases=purchases, current_Cash=current_Cash, startCash=startCash)


@views.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # transactions (user_id, symbol, shares, price, transacted)
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = (?)", (session['user_id'],)).fetchall()
    
    for i in range(len(transactions)):
        transactions[i] = list(transactions[i])
        transactions[i][3] = usd(transactions[i][3])

    return render_template("history.html", historys=transactions)


@views.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        symbol = request.form.get("symbol")
        if not symbol:
            flash("Missing symbol", category='error')
            return redirect("/quote")

        # Return {'name': x , 'price': x , 'symbol': x } if exsit
        quotes = lookup(symbol)
        if quotes == None:
            flash("Invalid symbol", category='error')
            return redirect("/quote")

        quotes['price'] = usd(quotes['price'])
        return render_template("quoted.html", quotes=quotes)

    return render_template("quote.html")



