import flask
from flask import Flask
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)


#江 10-30

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


#許 34-116
#可以選要開團or購物
@app.route("/home")
def home():
    return render_template("home.html")

#修改會員資料頁面( like edit in video ))
#輸入修改的資料
@app.route("/member_profile" , method=['POST' , 'GET'] )
def member_profile():
    if request.method == 'POST' :
        try:
            u_id = request.form['u_id']
            con = sqlite3.connect('DB.db')
            #con.row_factory = sqlite3.ROW
            cur = con.cursor()
            cur.execute("select rowid , * FROM user WHERE rowid = " + u_id )
            rows = cur.fetchall()
        except:
            u_id = None 
        finally:
            con.close()
            return render_template("member_profile.html")

#編輯的畫面(編輯頁)( like editrec )
#會員可修改畫面會跑出修改成功的畫面
@app.route("/edit", method=['POST', 'GET'])
def edit(): 
    if request.method == 'POST' :
        try:
            u_id = request.form['u_id']
            nm = request.form['nm']
            addr = request.form['addr']
            phone = request.form['phone']
            Bdate = request.form['Bdate']
            email = request.form['email']
            pw = request.form['pw']

            with sqlite3.connect('DB.db') as con :
                cur = con.cursor()
                cur.execute()
                cur.execute("UPDATE user SET user_id ='"+u_id+"' , username='"+nm+"' , address='"+addr+"' , phone='"+phone+"" , Bdate='"+Bdate+"' ,email='"+email+"' , password='"+pw+"' )
                con.commit()
                msg = "record successful " 
        except:
            #sth wrong 
            con.rollback()
            mas = "error!!" #where error
        finally:
            con.close()
            return render_template("result.html" , msg=msg )
#在要開團的畫面要輸入新商品的資料
@app.route("/grouping")
def grouping():
    return render_template("grouping.html")

#要把開團的商品加入倉庫並顯示成功
@app.route("/concern", methods=['POST','GET'])
def concern():
    if request.method == 'POST' :
        try:
            p_id = request.form['p_id']
            s_id = request.form['s_id']
            nm = request.form['nm']
            t_id = request.form['t_id']
            amount = request.form['amount']
            rele_date = request.form['rele_date']
            off_date = request.form['off_date']
            price = request.form['price']
            origin = request.form['origin']
            rating = request.form['rating']
            with sqlite3.connect('DB.db') as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO product ( product_id , seller_id , name , type_id , amount , release_date , off_date , price , origin , rating  ) VALUE( ?,?,?,?,?,?,?,?,?) ", ( p_id , s_id , nm , t_id , amount , rele_date , off_date , price , origin , rating ) ) 
                con.commit()
                msg = "record successful"
        except:
            con.rollback()
            msg = "error in insert "
        finally:
            con.close()
            return render_template('result.html' , msg = msg )

#浥118-281
# 總商品頁（四大項目）
@app.route("/product")
def product():
    return render_template("Shopping.html")

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