#浥 在四個種類的團購畫面加入團購商品到Shopping_Cart
from flask import Flask, request, render_template, redirect, url_for, session, make_response
import sqlite3
from app import app


# 總商品頁（四大項目）
@app.route("/product")
def product():
    return render_template("Shopping.html")

# type_id = 1, food
@app.route('/product/food')
def food():
    # Connect to the SQLite3 DB and
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    # 選擇種類為food的商品
    cur = con.cursor()
    cur.execute("SELECT product_id, * FROM Product WHERE type_id = 1")

    rows = cur.fetchall()
    con.close()

    return render_template("Food.html",rows=rows)

# type_id = 2, clothes
@app.route('/product/clothes')
def clothes():
    # Connect to the SQLite3 DB and
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    # 選擇種類為clothes的商品
    cur = con.cursor()
    cur.execute("SELECT product_id, * FROM Product WHERE type_id = 2")

    rows = cur.fetchall()
    con.close()

    return render_template("Clothes.html",rows=rows)

# type_id = 3, appliance
@app.route('/product/foapplianceod')
def applicances():
    # Connect to the SQLite3 DB
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    # 選擇種類為appliance的商品
    cur = con.cursor()
    cur.execute("SELECT product_id, * FROM Product WHERE type_id = 3")

    rows = cur.fetchall()
    con.close()

    return render_template("Applicances.html",rows=rows)

# type_id = 4, others
@app.route('/product/others')
def others():
    # Connect to the SQLite3 DB and
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    # 選擇種類為others的商品
    cur = con.cursor()
    cur.execute("SELECT product_id, * FROM Product WHERE type_id = 4")

    rows = cur.fetchall()
    con.close()

    return render_template("Others.html",rows=rows)


# 按 concern，回傳 shoppingCart
@app.route("/shoppingCart")
def shoppingCart():
    return render_template("ShoppingCart.html")

# 將商品加入購物車
@app.route('/add', methods=['POST'])
def add_product_to_cart():
    _amount = 1
    product_id = int (request.form['product_id'])
    # validate the received values
    if _amount and product_id and request.method == 'POST':

        # Connect to the SQLite3 DB and
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cursor.execute("SELECT * FROM Product WHERE product_id = ?", (product_id,))

        row = cursor.fetchone()
        con.close()
        itemArray = {str(row['product_id']): {'product_id': row['product_id'],'name': row['product_name'],'amount': int(_amount),'price': float(row['price'])}}
        # itemArray = { int(row['product_id']) : {'name' : row['product_name'], 'amount' : _amount, 'price': row['price']}}
        all_total_price = 0
        all_total_amount = 0

        session.modified = True
        if 'cart_item' in session:
            if row['product_id'] in session['cart_item']:
                for key, value in session['cart_item'].items():
                    if row['product_id'] == key:
                        old_amount = session['cart_item'][key]['amount']
                        total_amount = old_amount + _amount
                        session['cart_item'][key]['amount'] = total_amount
                        # session['cart_item'][key]['total_price'] = total_amount * row['price']
            else:
                session['cart_item'] = array_merge(session['cart_item'], itemArray)

            for key, value in session['cart_item'].items():
                individual_amount = int(session['cart_item'][key]['amount'])
                # individual_price = float(session['cart_item'][key]['total_price'])
                all_total_amount = all_total_amount + individual_amount
                # all_total_price = all_total_price + individual_price
        else:
            session['cart_item'] = itemArray
            all_total_amount = all_total_amount + _amount
            # all_total_price = all_total_price + _amount * row['price']

        session['all_total_amount'] = all_total_amount
        # session['all_total_price'] = all_total_price
        #四個種類return的頁面不一樣
        if row['type_id'] == 1:
            return redirect(url_for('food'))
        elif row['type_id'] == 2:
            return redirect(url_for('clothes'))
        elif row['type_id'] == 3:
            return redirect(url_for('applicances'))
        else:
            return redirect(url_for('others'))

    else:
        return 'Error while adding item to cart'

def array_merge( first_array , second_array ):
    if isinstance( first_array , list ) and isinstance( second_array , list ):
        return first_array + second_array
    elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
        return dict( list( first_array.items() ) + list( second_array.items() ) )
    elif isinstance( first_array , set ) and isinstance( second_array , set ):
        return first_array.union( second_array )
    return False


# 刪除購物車的物品
@app.route('/delete/<string:product_id>')
def delete_product(product_id):
    # print("Success the url")
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True

        # product_id = request.form.get('product_id')
        for item in session['cart_item'].items():
            if item[0] == product_id:
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['amount'])
                        # individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        # all_total_price = all_total_price + individual_price
                break

        if all_total_quantity == 0:
            session.clear()
        else:
            session['all_total_quantity'] = all_total_quantity
            # session['all_total_price'] = all_total_price
        # print("Success all")
        return redirect(url_for('shoppingCart'))
    except Exception as e:
        print(e)

@app.route("/buy" ,methods=['POST'])
def buy():
    print("url Success")
    # Connect to the SQLite3 DB and create a cursor
    con = sqlite3.connect("database.db")
    cursor = con.cursor()

    #拿到會員email和user_id(因為要存入order table中)
    email = session['email']
    cursor.execute('SELECT * FROM User WHERE email=?', (email,))
    user_id=cursor.fetchone()
    print("user id = ", user_id[0])
    
    #拿到locate資料存入locate table
    if request.method == "POST":
        print("POST success")
        address = request.form['address']
        print("address Success")
        phone = request.form['phone']
        print("address Success")
        print("address, phone",address, phone)
        # con.row_factory = sqlite3.Row
        
        cur = con.cursor()
        cur.execute('INSERT INTO Locate (address, phone) VALUES (?, ? );', (address, phone))
        con.commit()
        cur.execute('SELECT Locate_id FROM Locate Where address = ?', (address,))
        locate_id = cur.fetchone()[0]
        print("locate id = ", locate_id)
    
    #遍歷session['cart_item"]中的每個product_id
    for product_id in session['cart_item'].items():
        # print(session)
        # print("product_id = ",product_id[0])
        amount = int(session['cart_item'][product_id[0]].get('amount'))
        price = int(session['cart_item'][product_id[0]].get('price'))

        U_id = int(user_id[0])
        P_id = int(product_id[0])

        #check是否已經出現在table裡
        cursor.execute('SELECT * FROM Orders WHERE user_id=? and product_id=?', (U_id, P_id))
        existing_order=cursor.fetchone()

        if existing_order:
            #update已經有的record
            total_amount=existing_order[4]+amount
            cursor.execute('UPDATE Orders SET amount=? WHERE user_id=? and product_id=?',(total_amount, U_id, P_id))

        else:
            # Insert into the order table
            cursor.execute('INSERT INTO Orders ( user_id, product_id, price, locate_id, amount) VALUES ( ?, ?, ?, ?, ?)',( U_id ,P_id, price, locate_id, amount))

    # Commit the changes and close the connection
    con.commit()
    con.close()
    session.clear()

    # response = make_response('Buy successful')
    # return response
    return redirect(url_for('shoppingCart'))

#按shopping回到shopping.html編輯
@app.route("/Shopping")
def shopping():
     return render_template("Shopping.html")