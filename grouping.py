from flask import Flask, render_template, request, flash, redirect, url_for, session
import sqlite3
import sys
from app import app
con = sqlite3.connect("database.db", check_same_thread=False)

#在要開團的畫面要輸入新商品的資料
@app.route('/grouping' , methods=['POST','GET'])
def grouping():
    if request.method == 'POST' :
        nm = request.form['name']  # 產品名稱
        t_id = request.form['variety'] #產品種類
        amount = request.form['amount'] #數量
        price = request.form['price'] #價錢
        origin = request.form['origin'] #產地 
        seller_email = request.form['email'] #會員信箱        
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from User where email=? AND is_seller =?  " , ( seller_email , True ,  ))  #先確認是否db有這個email會員
        result = cur.fetchone()
        if result : #如果有 
            cur.execute( """    
                INSERT INTO Product ( 
                    seller_email, product_name, type_id, store, price, origin ) 
                VALUES
                    ( ?, ?, ?, ?, ?, ? ) 
                """, ( seller_email , nm , t_id , amount , price , origin )) 
            con.commit()
                # flash('Grouping  Success!') #利用 flash 顯示 開團成功 
        else:
            print( "nothing ")
            return "ERROR!! 可能原因: (1) 你並非賣家 (2) email 輸入錯誤  Try again ! "  
            #con.close()
    return render_template("Grouping.html") 