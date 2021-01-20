from flask import Flask, render_template, request, redirect, url_for, session
import csv
import sys
from ast import literal_eval
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/home")
def return_home():
    return render_template("home.html")

@app.route("/home", methods=["GET", "POST"])
def submit_email():
    if request.method == "GET":
        return redirect(url_for('home'))
    elif request.method == "POST":
        userdata = dict(request.form)
        email = userdata["email"]
        if(len(email) < 1):
            return render_template("home.html", status='* Please resubmit with valid information. *')
        else:
            with open('data/subscriberList.csv', mode='a', newline='') as file:
                data = csv.writer(file)
                data.writerow([email])
            return render_template("home.html", status='\\ Thank you for subscribing us! /')

@app.route("/login")
def login_page():
    return render_template("login.html")

# Read userInfo
@app.route('/login', methods=["POST"])
def login():
    userdata = dict(request.form)
    email = userdata["email"]
    password = userdata["password"]
    if(len(email) < 1 or len(password) < 1):
        return render_template("login.html", status="Invalid email or password.")
    with open('data/userInfo.csv') as file:
        data = csv.reader(file, delimiter=',')
        first_line = True
        user = []
        for row in data:
            if not first_line:
                if(row[3].strip() == email.strip() and row[5].strip() == password.strip()):
                    user.append({
                    "fname": row[0],
                    "email": row[3],
                    "password": row[5]
                    })
            else:
                first_line = False
    if(len(user) == 0):
        status = "Account does not exist. Please sign up first!"
    else:
        session['current_user'] = user
        session['logged_in'] = True
        status = "Login successful! Hello"
    return render_template("login.html", status=status, user=user)

@app.route("/signUp")
def signUp():
    return render_template("signUp.html")

# Add new user's sign up information into userInfo
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
        cart = []
        if(len(fname) < 1 or len(lname) < 1 or len(phoneNum) < 1 or len(email) < 1 or len(birthday) < 1 or len(password) < 1 or len(confirmPw) < 1):
            return render_template("signup.html", status='Please resubmit with valid information.')
        elif(password != confirmPw):
            return render_template("signup.html", status='* The entered password do not match. Please resubmit again.')
        else:
            with open('data/userInfo.csv', mode='a', newline='') as file:
                data = csv.writer(file)
                data.writerow([fname, lname, phoneNum, email, birthday, password, confirmPw, cart])
            return render_template("signup.html", status='Thank you for signing up!')

@app.route("/cart", methods=["GET", "POST"])
def getCart():
    if 'logged_in' in session:
        user = session.get('current_user')
        with open('data/userInfo.csv') as file:
            data = csv.reader(file, delimiter = ',')
            first_line = True
            cart = []
            for row in data:
                if not first_line:
                    if len(user) > 0:
                        if(row[3].strip() == user[0].get('email').strip()):
                            cart = row[7]
                else:
                    first_line = False
        print(cart, flush=True)
        return render_template("cart.html", status = "Success", cart = literal_eval(cart))
    status = "You are not logged in! Please login before adding any items to cart."
    return render_template("login.html", status=status)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/men")
def men():
    return render_template("men.html")

@app.route("/men", methods=["POST"])
@app.route("/women", methods=["POST"])
@app.route("/kids", methods=["POST"])
@app.route("/accessory", methods=["POST"])
def addToCart():
    user = session.get('current_user')
    item = request.form.to_dict()
    name = item["name"]
    image = item["image"]
    price = item["price"]
    file1 = open('data/userInfo.csv', 'rt')
    r = csv.reader(file1, delimiter=',')
    first_line = True
    data = []
    tem = []
    for row in r:
        if not first_line:
            if len(user) > 0:
                if(row[3].strip() == user[0].get('email').strip()):
                    temp = literal_eval(row[7])
                    #temp = row[7][1:-1].replace("'", '').strip().split(',')
                    temp.append([image, name, price])
                    hold = row[0:7]
                    hold.append(temp)
                    data.append(hold)
                else:
                    data.append(row)
        else:
            first_line = False
            data.append(row)
    file1.close()
    file2 = open('data/userInfo.csv', 'w')
    writer = csv.writer(file2,delimiter=',')
    writer.writerows(data)
    file2.close()
    return redirect(url_for('getCart'))

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

@app.route("/contactInfo")
def contactInfo():
    return render_template("contactInfo.html")

@app.route('/logout')
def logout():
    session.pop('current_user', None)
    return render_template("login.html", status="You have now logged out!")