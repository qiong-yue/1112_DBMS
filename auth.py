from flask import Flask, render_template, request, flash, redirect, url_for, session
import sqlite3
import sys
from app import app
con = sqlite3.connect("database.db", check_same_thread=False)


@app.route('/')
def index():
    return render_template("Log_In.html")
# @app.route('/login')
# def login():
#     return render_template('Log_In.html')


@app.route('/home')
def home():
    return render_template("Home.html")


@app.route('/profile')
def profile():
    return render_template('Member_Profile.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""
            SELECT
                *
            FROM
                User
            WHERE
                email= ? AND
                password= ?;
            """, (email, password))
        data = cur.fetchone()

        if data:
            session["email"] = data["email"]
            session["password"] = data["password"]
            return redirect(url_for("home"))
        else:
            return "Username and Password Mismatch"
    return render_template("Log_In.html")


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        try:
            email = request.form['email']
            password = request.form['password']
            bdate = request.form['bdate']
            phone = request.form['phone']
            address = request.form['address']

            con.row_factory = sqlite3.Row
            cur = con.cursor()
            print(cur, file=sys.stderr)
            cur.execute("select * from User where email= ?", (email,))
            result = cur.fetchone()
            print(result, file=sys.stderr)

            if result:
                print("already been used", file=sys.stderr)
                return redirect(url_for("register"))
            else:
                cur = con.cursor()
                cur.execute("""
                    INSERT INTO User (
                        address, phone, email, Bdate, password)
                    VALUES
                        (?, ?, ?, ?, ?);
                    """, (address, phone, email, bdate, password))
                con.commit()
                print("success", file=sys.stderr)
        except Exception:
            print("Error in Insert Operation", file=sys.stderr)
        finally:
            print("finished", file=sys.stderr)
            return redirect(url_for("index"))
    return render_template('Register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))
