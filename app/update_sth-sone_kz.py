from flask import Flask
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)

#起始點(登入)
@app.route("/")
def log_in():   
    return render_template("Log_in.html") 

#可以選要開團or購物
@app.route("/home")
def home():
    return render_template("Home.html")

#修改會員資料頁面( like edit in video ))
#輸入修改的資料
@app.route("/member_profile" , methods=['POST' , 'GET'] )
def member_profile():
    if request.method == 'POST' :
        try:
            email = request.form['email']   #找到要修改的email
            con = sqlite3.connect('database.db')
            #con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("select rowid , * FROM user WHERE rowid = " + email )  #找到那人的資料
            
            #rows = cur.fetchall()
        except:
            email = None 
        finally:
            con.close()
            return render_template("Member_Profile.html") #改網址名

#編輯的畫面(編輯頁)( like editrec )
#會員可修改畫面會跑出修改成功的畫面
@app.route("/edit", methods=['POST', 'GET'])
def edit(): 
    if request.method == 'POST' :
        try:
            #讀取需要修改會員的資料 ps. email 不可以改
            email = request.form['email']
            pw = request.form['password']
            Bdate = request.form['bdate']
            phone = request.form['phone']
            addr = request.form['address']
            # pw = request.form['pw']

            with sqlite3.connect('DB.db') as con :
                cur = con.cursor()    #以下是執行修改的動作
                cur.execute("UPDATE user SET  address='" +addr+"' , phone='"+phone+"' , Bdate='"+Bdate+"' , password='"+pw+"'  WhERE email = "+email )
                con.commit()
                msg = "record successful " 

        except:
            #sth wrong 
            con.rollback()
            mag = "error!!" #where error
        finally:   #如果沒有result的畫面就刪除，但不知道可不可以沒有return
            con.close()
            return render_template("result.html" , msg=msg )

#在要開團的畫面要輸入新商品的資料
@app.route("/grouping")
def grouping():
    return render_template("Grouping.html") #大寫 

#要把開團的商品加入倉庫並顯示成功
@app.route("/addProduct", methods=['POST','GET'])
def addProduct():
    if request.method == 'POST' :
        try:
            nm = request.form['name']  # 產品名稱
            t_id = request.form['variety']
            amount = request.form['amount']
            price = request.form['price']
            origin = request.form['origin']
            seller_email = request.form['email']
            with sqlite3.connect('DB.db') as con :
                cur = con.cursor()
                cur.execute(  #加入新商品資訊 
                    "INSERT INTO product ( seller_email , product_name , type_id , store  , price , origin  ) VALUE( ?,?,?,?,?,?) ", ( seller_email , nm , t_id , amount , price , origin  ) ) 
                con.commit()
                msg = "record successful"
        except:
            con.rollback()
            msg = "error in insert "
        finally:  #如果沒有result的畫面就刪除，但不知道可不可以沒有return 
            con.close()
            return render_template('result.html' , msg = msg )
        
        

