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
            return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signUp")
def signUp():
    return render_template("signUp.html")

@app.route("/signUp", methods=["GET", "POST"])
def save_user_data():
    if request.method == "GET":
        return redirect(url_for('signUp'))
    elif request.method == "POST":
        userdata = dict(request.form)
        fname = userdata["fname"]
        lname = userdata["lname"]
        phoneNum = userdata["phoneNum"]
        email = userdata["email"]
        birthday = userdata["bday"]
        password = userdata["password"]
        confirmPw = userdata["confirm-password"]
        if(len(fname) < 1 or len(lname) < 1 or len(phoneNum) < 1 or len(email) < 1 or len(birthday) < 1 or len(password) < 1 or len(confirmPw) < 1):
            return render_template("signup.html", status='Please resubmit with valid information.')
        elif(password != confirmPw):
            return render_template("signup.html", status='* The entered password do not match. Please resubmit again.')
        else:
            with open('data/signUpData.csv', mode='a', newline='') as file:
                data = csv.writer(file)
                data.writerow([fname, lname, phoneNum, email, birthday, password, confirmPw])
            return render_template("signup.html", status='Thank you for signing up!')

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