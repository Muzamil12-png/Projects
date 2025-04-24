import os
from cs50 import SQL
from flask import Flask, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # Validate input
        if not name or not month or not day:
            return render_template("apology.html", message="Must provide all fields"), 400

        # Insert into database using CS50 SQL syntax
        db.execute("INSERT INTO birthdays (name, month, day) VALUES (:name, :month, :day)",
                   name=name, month=month, day=day)

        return redirect("/")

    # Fetch all birthdays
    birthdays = db.execute("SELECT * FROM birthdays")
    return render_template("index.html", birthdays=birthdays)

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    db.execute("DELETE FROM birthdays WHERE id = :id", id=id)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
