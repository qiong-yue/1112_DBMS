import sqlite3
from flask import Flask, redirect, url_for, render_template, request, session, abort
import sys

app = Flask(__name__)
# 可以在這之後把自己的檔案名加進來
import auth
import category
import buy
import edit_profile
import grouping

app.secret_key = "secret"


if __name__ == '__main__':
    app.run(debug=True)