from flask import Flask, render_template, request
import csv
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

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

# @app.route("/subscribe")
# def submit_form():
#     userdata = dict(request.form)
#     email = userdata["email"]
#     if(len(email) < 1):
#         return render_template("home.html", status='Please resubmit with valid email.')
#     else:
#         with open('data/users.csv', mode='a', newline='') as file:
#             data = csv.writer(file)
#             data.writerows([email])
#         return render_template("home.html", status='Email successfully added to our list!')
