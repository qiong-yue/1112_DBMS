import flask
from flask import Flask, flash, redirect, url_for, request
from flask import render_template
from flask import request
from flask_login import UserMixin, LoginManager
from app import db, login
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
import wtforms, sqlite3
from flask_login import login_user, login_required, current_user, logout_user
from app import app, bcrypt, db
from app.forms import RegisterForm, LoginForm
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from config import Config



app = Flask(__name__)


#江 28-48

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


#許 50-133
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

#浥134-299
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


# 黃思：300~423
# 按下register，輸入data到member table，return login.html
@app.route("/addmember", methods=["POST", "GET"])
def addmember():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        fname = form.fname.data
        email = form.email.data
        pwd = bcrypt.generate_password_hash(form.pwd.data)
        bdate = request.form['bdate']
        phone = request.form['phone']
        adr = request.form['adr'] 
        user=User(user_id = user_id, username = fname, address = adr, phone=phone, Bdate=bdate, email=email, password=pwd)
        app.db.session.add(user)
        app.db.session.commit()
        flash('Congrates, registration success', category='success')    
        return redirect(url_for('index'))
    return render_template("Log_In.html", form=form)

# model.py
@login.user_loader
def load_user(user_id):
    return User.query.filter_by(user_id=user_id).first()

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    adr = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    bdate = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    pwd = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

# form.py
wtforms.BooleanField

class RegisterForm(FlaskForm):
    fname = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    pwd = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    bdate = StringField('Birth Date', validators=[DataRequired()])
    phone = StringField('Cellphone', validators=[DataRequired(), Length(10)])
    adr = StringField('Address(Country)', validators=[DataRequired(), Length(min=4, max=30)])
    recaptcha = RecaptchaField()
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already token, please choose another one. ')
class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    pwd = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Submit')

#route.py
@app.route("/")
@login_required
def home():
    return render_template("home.html")

@app.route("/Register", methods=["POST", "GET"])
def Register():
    if current_user.is_authentiated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        fname = form.fname.data
        email = form.email.data
        pwd = bcrypt.generate_password_hash(form.pwd.data)
        bdate = form.bdate.data
        phone = form.phone.data
        adr = form.adr.data 
        user=User(user_id = user_id, fname = fname, adr = adr, phone=phone, bdate=bdate, email=email, pwd=pwd)
        db.session.add(user)
        db.session.commit()
        flash('Congrates, registration success', category='success')    
        return redirect(url_for('home'))
    return render_template("Register.html", form=form)

@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authentiated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        pwd = form.pwd.data
        remember = form.remember.data
        # Check if pwd is matched
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.pwd, pwd):
            #user exists and pwd matched
            login_user(user, remember=remember)
            flash('Login success', category='info')
            if request.args.get('next'):
                next_page = request.args.get('next')
                return redirect(url_for(next_page))
            return redirect(url_for('home'))
        flash('User not exists or password not matched', category='danger')
    return render_template("Log_in.html", form=form)

@app.route('logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


#__init__.py
app = Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'You must login to access this page'
login.login_message_category = 'info'

from app.routes import *

#雯 427 - 500
#加table order 
conn.execute(
    "DROP TABLE order " )
conn.execute(
    'CREATE TABLE IF NOT EXISTS order(order_id INTEGER PRIMARY KEY , amount INTEGER ,date TEXT , product_id INTEGER ,  price INTEGER , coupon_status INTEGER ,locate_id INTEGER ) ')

#前端連接資料庫 在food四分頁裡
@app.route("/Shopping_Cart")
def Shopping_Cart():
    return  render_template("Shopping_Cart.html")

#buy加到order裡，請浥改這個
#itemArray = { row['product_id'] : {'name' : row['name'], 'amount' : _amount, 'price' : row['price'], 'total_price': _amount * row['price'],
                                           #'coupon_status': row['coupon_status'], 'locate_id': row['locate_id']}}
#coupon要留嗎
@app.route("/buy")
def buy(cart_items):
    order_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Connect to the SQLite3 DB and create a cursor
    con = sqlite3.connect("DB.db")
    cursor = con.cursor()
    
    for product_id, item in cart_items.items():
        order_id=None
        name = item['name']
        amount = item['amount']
        price = item['price']
        total_price = item['total_price']
        coupon_status = item['coupon_status']
        locate_id = item['locate_id']
        
        # Insert the item into the order table
        cursor.execute('INSERT INTO orders (order_id,date, product_id, name, price, amount, total_price, coupon_status, locate_id) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?)',
                       (order_id,order_date, product_id, name, price, amount, total_price, coupon_status, locate_id))
    
    # Commit the changes and close the connection
    con.commit()
    con.close()

# 刪除購物車商品(一次一個)
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

#按shopping回到shopping.html編輯
@app.route("/Shopping")
def Shopping():
    return render_template("Shopping.html")