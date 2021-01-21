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
                if row[3].strip() == email.strip() and row[5].strip() == password.strip():
                    user.append({
                        "fname": row[0],
                        "lname": row[1],
                        "phoneNum": row[2],
                        "email": row[3],
                        "birthday": row[4],
                        "password": row[5],
                        "confirm-pw": row[6],
                        "cart": row[7]
                    })
            else:
                first_line = False
    if(len(user) == 0):
        status = "Account does not exist. Please check your email/password or sign up first!"
    else:
        session['current_user'] = user
        status = "Login successful! Welcome!"
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
            with open('data/userInfo.csv') as file:
                data = csv.reader(file, delimiter=',')
                first_line = True
                for row in data:
                    if not first_line:
                        if(row[3].strip() == email):
                            return render_template("signup.html", status='Sorry, this email has been registered by others. Please register your email with unregistered email instead.')
                    else:
                        first_line = False
            with open('data/userInfo.csv', mode='a', newline='') as file:
                data = csv.writer(file)
                data.writerow([fname, lname, phoneNum, email, birthday, password, confirmPw, cart])
            return render_template("signup.html", status='Thank you for signing up!')

@app.route("/cart", methods=["GET"])
def getCart():
    if 'current_user' in session:
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
        total = sum(float(item[2][1:]) for item in literal_eval(str(cart)))
        return render_template("cart.html", status = "Success", cart = literal_eval(cart), total = total)
    return render_template("login.html", status="You are not logged in! Please login before adding any items to cart.")

@app.route("/cart", methods=["POST"])
def deleteCart():
    if 'current_user' in session:
        user = session.get('current_user')
        itemdata = dict(request.form)
        index = itemdata["index"]
        file1 = open('data/userInfo.csv', 'rt')
        r = csv.reader(file1, delimiter=',')
        first_line = True
        data = []
        for row in r:
            if not first_line:
                if len(user) > 0:
                    if(row[3].strip() == user[0].get('email').strip()):
                        temp = literal_eval(row[7])
                        temp.pop(int(index))
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
    return render_template("login.html", status="You are not logged in! Please login before adding any items to cart.")

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
    if 'current_user' in session:
        user = session.get('current_user')
        item = request.form.to_dict()
        name = item["name"]
        image = item["image"]
        price = item["price"]
        file1 = open('data/userInfo.csv', 'rt')
        r = csv.reader(file1, delimiter=',')
        first_line = True
        data = []
        for row in r:
            if not first_line:
                if len(user) > 0:
                    if(row[3].strip() == user[0].get('email').strip()):
                        temp = literal_eval(row[7])
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
        print(user)
        return redirect(url_for('getCart'))
    return render_template("login.html", status="You are not logged in! Please login before adding any items to cart.")

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

@app.route('/account')
def accountInfo():
    if 'current_user' in session:
        user = session.get('current_user')
        return render_template("account.html", user=user)
    return render_template("login.html", status="You are not logged in! Please login before viewing account setting.")

@app.route('/account', methods=["POST"])
def accountInfo_Update():
    if 'current_user' in session:
        user = session.get('current_user')
        user_fname = user[0].get('fname').strip()
        user_pw = user[0].get('password').strip()
        user_email = user[0].get('email').strip()
        data=[]
        userdata = dict(request.form)
        fname = userdata["fname"]
        lname = userdata["lname"]
        phoneNum = userdata["phoneNum"]
        email = userdata["email"]
        birthday = userdata["bday"]
        oldPw = userdata["old-password"]
        newPw = userdata["new-password"]
        confirmNewPw = userdata["confirm-password"]
        changingPw = len(newPw) > 0 and len(confirmNewPw) > 0
        updatedInfo=[]
        if oldPw != user[0].get('password').strip():
            return render_template("account.html", status="You have entered incorrectly for current password. Please check again.",user=user)
        if newPw != confirmNewPw:
            return render_template("account.html", status="The update password information does not match. Please resubmit again.",user=user)
        if oldPw == newPw:
            return render_template("account.html", status="The update password information should not be the same as the old password. Please resubmit again.",user=user)
        with open('data/userInfo.csv') as file:
            r = csv.reader(file, delimiter = ',')
            first_line = True
            for row in r:
                if not first_line:
                    if len(user) > 0:
                        if(row[3].strip() == email and row[3].strip() != user_email):
                            return render_template("account.html", status='Sorry, this email has been registered by others. Please update your new email with unregistered email instead.',user=user)
                        if(row[0].strip() == user_fname):
                            user_cart = literal_eval(row[7])
                            if changingPw:
                                data = [fname,lname,phoneNum,email,birthday,newPw,confirmNewPw,user_cart]
                                user.insert(0, {
                                    "fname": fname,
                                    "lname": lname,
                                    "phoneNum": phoneNum,
                                    "email": email,
                                    "birthday": birthday,
                                    "password": newPw,
                                    "confirm-pw": confirmNewPw,
                                    "cart": user_cart
                                })
                            else:
                                data = [fname,lname,phoneNum,email,birthday,user_pw,user_pw,user_cart]
                                user.insert(0, {
                                    "fname": fname,
                                    "lname": lname,
                                    "phoneNum": phoneNum,
                                    "email": email,
                                    "birthday": birthday,
                                    "password": user_pw,
                                    "confirm-pw": user_pw,
                                    "cart": user_cart
                                })
                        else:
                            updatedInfo.append(row)
                else:
                    first_line = False
                    updatedInfo.append(row)
        clearFile = open("data/userInfo.csv", "w")
        clearFile.truncate()
        clearFile.close()
        with open('data/userInfo.csv', mode='a', newline='') as file:
            writer=csv.writer(file)
            writer.writerows(updatedInfo)
            writer.writerow(data)
        if len(user) > 1:
            user.pop()
        return render_template("account.html", user=user, status="Account Info successfully updated!")
    return render_template("login.html", status="You are not logged in! Please login before viewing account setting.")

@app.route('/logout')
def logout():
    if 'current_user' in session:
        session.pop('current_user', None)
        return render_template("login.html", status="You have now logged out!")
    return render_template("login.html", status="You are unable to logout since you haven't login yet.")