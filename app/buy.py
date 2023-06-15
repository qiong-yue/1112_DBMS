from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)

@app.route("/ShoppingCart")
def Shopping_Cart():
    return  render_template("ShoppingCart.html")

#buy加到order裡，order_id改user_id，改merge
@app.route("/buy")
def buy(cart_items):
    
    # Connect to the SQLite3 DB and create a cursor
    con = sqlite3.connect("database.db")
    cursor = con.cursor()

    #shopping cart裡加user_id, locate_id!!!!!!!!!!!!!!
    for (product_id, user_id), item in cart_items.items():
        amount = item['amount']#如果要記的是總數就要在shopping cart裡加totaol_amount
        price = item['price']
        locate_id = item['locate_id']
        
        # Insert the item into the order table 
        cursor.execute('INSERT INTO orders ( user_id,product_id, price, amount, locate_id) VALUES ( ?, ?, ?, ?, ?)',
                       ( user_id ,product_id, price, amount, locate_id))
    
    order_id+=1
    # Commit the changes and close the connection
    con.commit()
    con.close()


#按shopping回到shopping.html編輯
@app.route("/Shopping")
def Shopping():
    return render_template("Shopping.html")