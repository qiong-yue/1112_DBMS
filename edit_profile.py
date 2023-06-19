from flask import Flask
from flask import render_template
from flask import request
import sqlite3
from flask import flash  # 利用flash  
from app import app


#修改會員資料頁面( like edit in video ))
#輸入修改的資料
@app.route("/member_profile" , methods=['POST' , 'GET'] )
def member_profile():
    if request.method == 'POST' :
        try:
            email = request.form['email']   #找到要修改的email
            con = sqlite3.connect('DataBase.db')
            #con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select rowid , * FROM user WHERE rowid = " +email )  #找到那人的資料

            #rows = cur.fetchall()
        except:
            email = None 
        finally:
            con.close()
            return render_template("member_profile.html") #改網址名
        
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
            with sqlite3.connect('Database.db') as con :
                cur = con.cursor()    #以下是執行修改的動作
                cur.execute("UPDATE user SET  address='" +addr+"' , phone='"+phone+"' , Bdate='"+Bdate+"' , password='"+pw+"'  WhERE email = "+email )
                con.commit()
                flash('Edit Success!')  # 利用flash 表示 修改成功 
        except:
            #sth wrong 
            con.rollback()
            flash('Edit ERROR !') # 利用 flash 傳送修改錯誤
        finally: 
            con.close()
        


