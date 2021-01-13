from flask import Flask, render_template
import csv
app = Flask(__name__)

@app.route("/")
def homePage():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signUp")
def signUp():
    return render_template("signup.html")