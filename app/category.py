#浥 在四個種類的團購畫面加入團購商品到Shopping_Cart
from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)

# 總商品頁（四大項目）
@app.route("/product")
def product():
    return render_template("product.html")

# type_id = 1, food
@app.route('/product/food')
def food():
    # Connect to the SQLite3 DB and 
    con = sqlite3.connect("DB.db")
    con.row_factory = sqlite3.Row

    # 選擇種類為food的商品
    cur = con.cursor()
    cur.execute("SELECT product_id, * FROM product WHERE type_id = 1")

    rows = cur.fetchall()
    con.close()

    return render_template("food.html",rows=rows)

# type_id = 2, clothes
@app.route('/product/clothes')
def clothes():
    # Connect to the SQLite3 DB and 
    con = sqlite3.connect("DB.db")
    con.row_factory = sqlite3.Row

    # 選擇種類為clothes的商品
    cur = con.cursor()
    cur.execute("SELECT product_id, * FROM product WHERE type_id = 2")

    rows = cur.fetchall()
    con.close()

    return render_template("clothes.html",rows=rows)

# type_id = 3, appliance
@app.route('/product/foapplianceod')
def appliance():
    # Connect to the SQLite3 DB 
    con = sqlite3.connect("DB.db")
    con.row_factory = sqlite3.Row

    # 選擇種類為appliance的商品
    cur = con.cursor()
    cur.execute("SELECT product_id, * FROM product WHERE type_id = 3")

    rows = cur.fetchall()
    con.close()

    return render_template("appliance.html",rows=rows)

# type_id = 4, others
@app.route('/product/others')
def others():
    # Connect to the SQLite3 DB and 
    con = sqlite3.connect("DB.db")
    con.row_factory = sqlite3.Row

    # 選擇種類為others的商品
    cur = con.cursor()
    cur.execute("SELECT product_id, * FROM product WHERE type_id = 4")

    rows = cur.fetchall()
    con.close()

    return render_template("others.html",rows=rows)


# 按 concern，回傳 shoppingCart
@app.route("/shoppingCart")
def shoppingCart():
    return render_template("shoppingCart.html")

# 將商品加入購物車
@app.route('/add', methods=['POST'])
def add_product_to_cart():
    _amount = int(request.form['amount'])
    product_id = request.form['product_id']
    # validate the received values
    if _amount and product_id and request.method == 'POST':

        # Connect to the SQLite3 DB and 
        con = sqlite3.connect("DB.db")
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cursor.execute('SELECT * FROM product WHERE product_id = %d', (product_id,))

        row = cursor.fetchone()
        con.close()
        itemArray = { row['product_id'] : {'name' : row['name'], 'amount' : _amount, 'price' : row['price'], 'total_price': _amount * row['price']}}

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
                        session['cart_item'][key]['total_price'] = total_amount * row['price']
            else:
                session['cart_item'] = array_merge(session['cart_item'], itemArray)
        
            for key, value in session['cart_item'].items():
                individual_amount = int(session['cart_item'][key]['amount'])
                individual_price = float(session['cart_item'][key]['total_price'])
                all_total_amount = all_total_amount + individual_amount
                all_total_price = all_total_price + individual_price
        else:
            session['cart_item'] = itemArray
            all_total_amount = all_total_amount + _amount
            all_total_price = all_total_price + _amount * row['price']
            
        session['all_total_amount'] = all_total_amount
        session['all_total_price'] = all_total_price
                
        return redirect(url_for('products'))
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
@app.route('/delete')
def delete_product(product_id):
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True
        
        for item in session['cart_item'].items():
            if item[0] == product_id:    
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                break
        
        if all_total_quantity == 0:
            session.clear()
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
            
        return redirect(url_for('.products'))
    except Exception as e:
        print(e)