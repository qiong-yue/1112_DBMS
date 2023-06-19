from flask import Flask
from flask import render_template
from flask import request
from flask import session,redirect, url_for

import sqlite3
from flask import flash  # 利用flash  
from app import app
import sys


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
            cur.execute("select rowid , * FROM user WHERE rowid = " +email )  #找到那人的資料

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
            with sqlite3.connect('database.db') as con :
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
        

@app.route("/delete_member", methods=["POST", "GET"])
def delete_member(): 
    # print("not request method",  file=sys.stdout)
    if request.method == "GET":
        try:
            print("in request method",  file=sys.stdout)
            print("try to delete", file=sys.stdout);
            #讀取需要修改會員的資料
            email = session['email']
            with sqlite3.connect('database.db') as con :
                cur = con.cursor()    #以下是執行修改的動作
                cur.execute("DELETE FROM User WHERE email = '" +email+"'")
                con.commit()
                session.clear()
                print("delete success", file=sys.stdout);
                return redirect(url_for("login")) # 利用flash 表示 修改成功 
        except:
            #sth wrong 
            print("except");
            con.rollback()
            return "delete ERROR!" # 利用 flash 傳送修改錯誤
        finally: 
            con.close()
            # return "close"
    return 0
        # return render_template("Log_In.html")