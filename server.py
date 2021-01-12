from flask import Flask, render_template
import csv
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")
