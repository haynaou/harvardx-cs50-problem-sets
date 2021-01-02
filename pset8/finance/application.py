import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""

    if request.method == "GET":
        # Get shares that belong to the user
        rows = db.execute("SELECT company_name, symbol, quantity FROM shares WHERE user_id =? ", session["user_id"])

        # Loop through shares and lookup the current price for each share and calculate the total price
        shares = []
        for row in rows:
            quote = lookup(row['symbol'])
            share = {
                'company_name': row['company_name'],
                'symbol': row['symbol'],
                'quantity': row['quantity'],
                'current_price': round(quote['price'], 2),
                'total': round(int(row['quantity']) * quote['price'], 2),
            }
            shares.append(share)

        # Calucalte how much cash the user currently owns
        rows = db.execute("SELECT cash from users WHERE id = ?", session["user_id"])
        existing_cash = round(rows[0]['cash'], 2)
        total = round(existing_cash + sum(share['total'] for share in shares), 2)

        return render_template("index.html", shares = shares, cash = existing_cash, total = total)

    if request.method == "POST":
        cash = request.form.get('cash')

        # Validate cash
        if cash == '' or int(cash) <= 0:
            return apology("Invalid amount", 400)
        cash = int(cash)

        # Update user cash by getting existing cash and adding new cash value
        rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        exiting_cash = rows[0]['cash']

        new_cash = exiting_cash + cash
        row_id = db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])
        if row_id == None:
            return apology("Cannot add cash", 500)

        # Return succesfful response
        flash('Cash added!')
        return redirect("/")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "GET":
        return render_template("buy.html")

    if request.method == "POST":
        shares = request.form.get("shares")
        symbol = request.form.get("symbol")

        # Validate shares
        if shares == '' or int(shares) <= 0:
            return apology("must provide valid number of shares", 403)
        shares = int(shares)

         # Validate symbol
        if not symbol or symbol == '':
            return apology("must provide symbol", 403)

        # Ensure lookup for symbol is successfful
        quote = lookup(symbol)
        if quote == None:
            return apology("No quote available for given symbol", 403)


        # Perform buy action:
        # Get existing cash for user.
        rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        existing_cash = rows[0]['cash']

        # Check if user can afford to buy shares
        if quote['price'] * shares > existing_cash:
            return apology("Not enough cash to buy the shares", 403)

        # Substract and update existing cash by amount bought
        existing_cash = existing_cash - (quote['price'] * shares)
        row_id = db.execute("UPDATE users SET cash = ? WHERE id = ?", existing_cash, session["user_id"])
        if row_id == None:
            return apology("Cannot perform transaction", 500)

        # Record transaction and return error if it fails
        row_id = db.execute("INSERT INTO transactions(created, user_id, company_name, symbol, quantity, price) values(datetime('now'),?,?,?,?,?)",
            session["user_id"], quote['name'], quote['symbol'], shares, quote['price'])
        if row_id == None:
            return apology("Cannot perform transaction", 500)

        # Update existing shares for user:
        # First, get the existing shares
        rows = db.execute("SELECT symbol, quantity FROM shares WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)

        # If user already owns the shares of symbol, we update existing quantity by incrementing it by new quantity
        if len(rows) != 0:
            print("user already owns symbol")
            existing_quantity = int(rows[0]['quantity'])
            new_quantity = existing_quantity + shares

            # Update existing quantity with new quantity
            row_id = db.execute("UPDATE shares SET quantity = ? WHERE user_id = ? AND symbol = ?",
                new_quantity, session["user_id"], quote['symbol'])
            if row_id == None:
                return apology("Cannot perform transaction", 500)

        # If user doesn't owns the shares of symbol, we insert new row with the new quantity
        else:
            print("user doesn't own symbol")
            row_id = db.execute("INSERT INTO shares(user_id, company_name, symbol, quantity) VALUES(?,?,?,?)",
                session["user_id"], quote['name'], quote['symbol'], shares)
            if row_id == None:
                return apology("Cannot perform transaction", 500)

        # Return successfful response
        flash('Bought!')
        return redirect("/")


@app.route("/history", methods=["GET"])
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT symbol, quantity, price, created FROM transactions WHERE user_id = ?", session['user_id'])
    return render_template('history.html', transactions = rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":
        return render_template("quote.html")

    if request.method == "POST":
        symbol = request.form.get("symbol")

        # Validate symbol
        if not symbol or symbol == '':
            return apology("Invalid symbol", 400)

        # Get quote and check for error
        quote = lookup(symbol)
        if quote == None:
            return apology("Unable to get quote", 400)

        return render_template("quoted.html",
            name=quote['name'], price=quote['price'], symbol=quote['symbol'])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate username
        if not username or username == '':
            return apology("Must provide username", 403)

        # Validate password
        if not password or password == '':
            return apology("Must provide password", 403)

        # Validate password confirmation
        if not confirmation or confirmation == '':
            return apology("Must provide password confirmation", 403)

        # Ensure password and password confirmation match
        if confirmation != password:
            return apology("Password and password confirmation do not match", 403)

        # Ensure username doesn't already taken
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) == 1:
            return apology("Username already taken", 400)

        # Create new user
        db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, generate_password_hash(password))

        # Redirect user to login page
        return redirect("/login")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == 'GET':
        # Get a list of existing symbols to show in sell form
        rows = db.execute("SELECT symbol FROM shares WHERE user_id = ?", session["user_id"])

        symbols = []
        for row in rows:
            symbols.append(row['symbol'])

        return render_template('sell.html', symbols = symbols)


    if request.method == "POST":
        shares = request.form.get("shares")

        # Validate shares
        if shares == '' or int(shares) <= 0:
            return apology("Enter a valid number", 400)

        shares = int(shares)

        # Validate symbol
        symbol = request.form.get("symbol")
        if symbol == None or symbol == '':
            return apology("Enter a valid symbol", 400)

        # Get current shares of the user
        rows = db.execute("SELECT quantity FROM shares WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
        if len(rows) == 0:
            return apology(f"You don't own any {symbol} shares", 403)

        # Check if user has enough shares
        existing_shares = int(rows[0]['quantity'])
        if existing_shares < shares:
            return apology("Not enough shares to sell", 400)

        # Lookup current symbol price
        quote = lookup(symbol)
        if quote == None:
            return apology(f"Cannot lookup price for {symbol}", 400)

        current_price = quote["price"]

        # Caluclate transaction total
        transaction_total = current_price * shares

        # Update existing user cash with new cash after selling the shares
        # First, get existing cash
        rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        existing_cash = rows[0]['cash']
        new_cash = transaction_total + existing_cash
        # Update existing cash
        row_id = db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])
        if row_id == None:
            return apology("Cannot perform transaction", 500)

        # Record transaction with "-" to mark as a sell
        row_id = db.execute("INSERT INTO transactions(created, user_id, company_name, symbol, quantity, price) VALUES(datetime('now'),?,?,?,?,?)",
            session["user_id"], quote['name'], quote['symbol'], -shares, quote['price'])
        if row_id == None:
            return apology("Cannot perform transaction", 500)

        # Update user shares
        new_quantity = existing_shares - shares

        # Remove share record if the new quantity is 0 (we no longer have any shares)
        if new_quantity == 0:
            row_id = db.execute("DELETE FROM shares WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
            if row_id == None:
                return apology("Cannot perform transaction", 500)
        # Update share quantity if new quantity is > 0
        else:
            row_id = db.execute("UPDATE shares SET quantity = ? WHERE user_id = ? AND symbol = ?", new_quantity, session["user_id"], symbol)
            if row_id == None:
                return apology("Cannot perform transaction", 500)

        flash('Sold!')
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
