from flask import Flask, render_template
import csv
app = Flask(__name__)

@app.route("/")
<<<<<<< HEAD
def index():
    return render_template("index.html")
=======
def homePage():
    return render_template("home.html")
>>>>>>> update server by adding home.html and removing the index.html(so that opening the website will be home page instead bec. index.html only has header and footer)

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signUp")
def signUp():
    return render_template("signup.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/about")
def about():
    return render_template("about.html")