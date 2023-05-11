import flask
from flask import Flask
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)



@app.route("/login")
def login():
    return render_template("Log_In.html")
@app.route("/checkmember", methods=["POST", "GET"])
def checkmember():
    return render_template("Member_Profile.html")


@app.route("/member")
def member():
    return render_template("Member_Profile.html")

@app.route("/register")
def register():
    return render_template("Register.html")
@app.route("/addmember", methods=["POST", "GET"])
def addmember():
    return render_template("Log_In.html")

