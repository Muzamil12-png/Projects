import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Database connection function
def get_db():
    conn = sqlite3.connect("finance.db")  # CS50 uses finance.db
    conn.row_factory = sqlite3.Row  # Allows fetching rows as dictionaries
    return conn

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
#def index():
#    """Show portfolio of stocks"""
#    return apology("TODO")
def index():
    stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", session["user_id"])
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    for stock in stocks:
        stock_info = lookup(stock["symbol"])
        stock["price"] = stock_info["price"]
        stock["total_value"] = stock["total_shares"] * stock["price"]

    grand_total = user_cash + sum(stock["total_value"] for stock in stocks)

    return render_template("index.html", stocks=stocks, cash=user_cash, total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
#def buy():
#    """Buy shares of stock"""
#    return apology("TODO")

def buy():
    symbol = request.form.get("symbol")
    shares = request.form.get("shares")

    if not symbol or not shares.isdigit() or int(shares) <= 0:
        return render_template("apology.html", message="Invalid input")

    stock = lookup(symbol)
    if not stock:
        return render_template("apology.html", message="Stock not found")

    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    cost = int(shares) * stock["price"]

    if cost > user_cash:
        return render_template("apology.html", message="Not enough funds")

    db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
               session["user_id"], symbol, int(shares), stock["price"])
    db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, session["user_id"])

    return redirect("/")


@app.route("/history")
@login_required
#def history():
#    """Show history of transactions"""
#    return apology("TODO")
def history():
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", transactions=transactions)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
#def quote():
#    """Get stock quote."""
#   return apology("TODO")
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)

        if not stock:
            return render_template("apology.html", message="Invalid stock symbol")

        return render_template("quoted.html", stock=stock)

    return render_template("quote.html")

def lookup(symbol):
    """Look up stock price using an API (e.g., IEX Cloud, Alpha Vantage)"""
    response = requests.get(f"https://api.example.com/stock/{symbol}")
    if response.status_code != 200:
        return None
    return response.json()


#@app.route("/register", methods=["GET", "POST"])
#def register():
#    """Register user"""
#    return apology("TODO")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate input (Check for empty fields)
        if not username or not password or not confirmation:
            return render_template("apology.html", message="Must fill all fields"), 400

        # Check if passwords match
        if password != confirmation:
            return render_template("apology.html", message="Passwords do not match"), 400

        # Hash the password
        hashed_password = generate_password_hash(password)

        try:
            db = get_db()
            cursor = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hashed_password))
            db.commit()

            # Log the user in automatically after successful registration
            session["user_id"] = cursor.lastrowid

            return redirect("/")

        except sqlite3.IntegrityError:  # Catch duplicate username error
            return render_template("apology.html", message="Username already exists"), 400

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
#def sell():
#    """Sell shares of stock"""
#    return apology("TODO")
def sell():
    symbol = request.form.get("symbol")
    shares = int(request.form.get("shares"))

    user_shares = db.execute("SELECT SUM(shares) as total FROM transactions WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)[0]["total"]

    if shares > user_shares:
        return render_template("apology.html", message="Not enough shares")

    stock = lookup(symbol)
    revenue = shares * stock["price"]

    db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", session["user_id"], symbol, -shares, stock["price"])
    db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", revenue, session["user_id"])

    return redirect("/")
