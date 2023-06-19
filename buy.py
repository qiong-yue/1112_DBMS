from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
from app import app

# @app.route("/ShoppingCart")
# def ShoppingCart():
#     return  render_template("ShoppingCart.html")

#buy加到order裡，如果已經在order裡就改merge、update
#如果還沒就insert
                    
@app.route("/buy")
def buy(cart_items):
    
    # Connect to the SQLite3 DB and create a cursor
    con = sqlite3.connect("DB.db")
    cursor = con.cursor()

    #shopping cart裡加user_id, locate_id!!!!!!!!!!!!!!

    for (product_id, user_id), item in cart_items.items():
        amount = item['amount'] #如果要記的是總數就要在shopping cart裡加totaol_amount
        price = item['price']
        locate_id = item['locate_id']
        
        #check是否已經出現在table裡
        cursor.execute('SELECT * FROM orders WHERE user_id=? and product_id=?', (user_id, product_id))
        existing_order=cursor.fetchone()
        
        if existing_order:
            #update已經有的record
            total_amount=existing_order[4]+amount
            cursor.execute('UPDATE orders SET amount=? WHERE user_id=? and product_id=?',(total_amount, user_id, product_id))

        else:
            # Insert into the order table 
            cursor.execute('INSERT INTO orders ( user_id,product_id, price, locate_id,amount) VALUES ( ?, ?, ?, ?, ?)',
                           ( user_id ,product_id, price, locate_id,amount))
    
    # Commit the changes and close the connection
    con.commit()
    con.close()


#按shopping回到shopping.html編輯
@app.route("/Shopping")
def shopping():
     return render_template("Shopping.html")