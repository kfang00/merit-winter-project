from flask import Flask, render_template, request, redirect, url_for
import csv
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/home", methods=["GET", "POST"])
def submit_email():
    if request.method == "GET":
        return redirect(url_for('home'))
    elif request.method == "POST":
        userdata = dict(request.form)
        email = userdata["email"]
        if(len(email) < 1):
            return render_template("home.html", status='Please resubmit with valid information.')
        else:
            with open('data/subscriberList.csv', mode='a', newline='') as file:
                data = csv.writer(file)
                data.writerow([email])
            return render_template("home.html", status='You have been added to our subscribe list!')

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

@app.route("/men")
def men():
    return render_template("men.html")

@app.route("/women")
def women():
    return render_template("women.html")

@app.route("/accessory")
def accessory():
    return render_template("accessory.html")

@app.route("/kids")
def kids():
    return render_template("kids.html")

@app.route("/help")
def help():
    return render_template("help.html")