from flask import Flask , redirect , url_for 
from flask import render_template
from flask import request
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
    if request.method == 'POST' :
        email = request.form['email']   #找到要修改的email
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(""" 
            SELECT  
                * 
            FROM 
                User 
            WHERE 
                email=? ;
            """ , (email , ) ) #找到那人的資料
        data = cur.fetchone()

        if data :
            pw = request.form['password']  
            Bdate = request.form['bdate']
            phone = request.form['phone']
            addr = request.form['address']
            cur = con.cursor()    #以下是執行修改的動作
            cur.execute( "UPDATE User SET address=? , phone=? , Bdate=? , password=? , WHERE email=? " ,( addr , phone , Bdate , pw , email ) )
            con.commit()
            flash('Edit Success!')
            return redirect(url_for("index"))
        else:
            return "email can not edit !!!"
    return render_template("Log_In.html") #改網址名
        


