from flask import Flask, render_template, request, redirect, url_for
import csv
app = Flask(__name__)

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
        users = []
        for row in data:
            if not first_line:
                if(row[3].strip() == email.strip() and row[5].strip() == email.strip()):
                    users.append({
                    "fname": row[0],
                    "email": row[1],
                    "password": row[2]
                    })
            else:
                first_line = False
    if(len(users) == 0):
        status = "Account does not exist. Please sign up first!"
    else:
        status = "Login successful!"
    return render_template("login.html", status=status, users=users)

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
        if(len(fname) < 1 or len(lname) < 1 or len(phoneNum) < 1 or len(email) < 1 or len(birthday) < 1 or len(password) < 1 or len(confirmPw) < 1):
            return render_template("signup.html", status='Please resubmit with valid information.')
        elif(password != confirmPw):
            return render_template("signup.html", status='* The entered password do not match. Please resubmit again.')
        else:
            with open('data/userInfo.csv', mode='a', newline='') as file:
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

@app.route("/contactInfo")
def contactInfo():
    return render_template("contactInfo.html")