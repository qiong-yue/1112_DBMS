from flask import Flask , redirect , url_for 
from flask import render_template
from flask import request, session
import sqlite3
import sys 
from flask import flash  # 利用flash  
from app import app
con = sqlite3.connect("database.db" , check_same_thread=False )


@app.route('/member_profile' )
def member_profile():
    return render_template("Member_Profile.html")

#輸入修改的資料
@app.route( '/edit' , methods=['POST' , 'GET'] )
def edit():
    print( "enter")
    if request.method == 'POST' :
        try:
            email = session.get('email')
            print(email)
            pw = request.form['password']  
            Bdate = request.form['bdate']
            phone = request.form['phone']
            addr = request.form['address']
            #以下是執行修改的動作
            print(pw)
            print(Bdate)
            print(phone)
            print(addr)
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE User SET address='"+addr+"', phone='"+phone+"', Bdate='"+Bdate+"', password='"+pw+"' WHERE email='"+email+"'")
                con.commit()
            flash('Edit Success!')
            return redirect(url_for("index"))
        except:
            con.rollback()
        finally:
            con.close()
    return render_template("Log_In.html") #改網址名
        

      
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

