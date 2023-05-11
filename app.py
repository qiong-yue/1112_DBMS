import flask
from flask import Flask
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)


#江 10-30
#登入
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


#許 32-114
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