from flask import flash, redirect, render_template, request, session, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from .helpers import db
from finance.model.database import Cash, User



"""  for authentication , Three routes in this blueprint ===>   /login    /logout    /register  """

# Create blueprint
auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        user_name = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not user_name or not password :
            flash('Must provide username and password', category='error')
            return render_template("login.html")

        # --------------------------------------------------------------------------------

        # TABLE ====> users (id, username, hash, cash)
        # Query database for username  ============> return list[] with tuble () if exist
        user = db.execute("SELECT * FROM users WHERE username = ?", (user_name,)).fetchall()

        # Check if we have username, then check match hash wih password
        if len(user) == 1 :
            if check_password_hash(user[0][2], password):

                flash('Logged in successfully!', category='success')
                # Remember which user has logged in
                session["user_id"] = user[0][0]
                return redirect("/")
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html")


@auth.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@auth.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # -------------------------------------------------------------------------------- 

        username = request.form.get("username")
        # """users (id, username, hash, cash)"""
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()

        # If not username or already exsit  ======= len() work with list[] not tuble ()
        if not username or len(user) != 0:
            flash('Invalid username', category='error')
            return redirect("/register")

        # --------------------------------------------------------------------------------

        # Check if passwords blank or don't match
        password = request.form.get("password")
        confirm = request.form.get("confirmation")

        if not password or not confirm:
            flash('Missing password', category='error')
            return redirect("/register")

        if password != confirm:
            flash("Passwords don't match", category='error')
            return redirect("/register")

        # --------------------------------------------------------------------------------

        # INSERT the new user into users, storing a hash of the user’s password
        hash_psw = generate_password_hash(password)
        
        # Return [] of id & cash of inserted user
        id_cash = User.add(username, hash_psw)
        user_id   = id_cash[0]
        startCash = id_cash[1]

        # LINK the user TABLE with ==> cash TABLE <== to keep track of currentCash
        Cash.set_Current_Cash(user_id, startCash)

        session["user_id"] = user_id
        return redirect("/")

    return render_template("register.html")

