from flask import Flask
from flask import render_template
from flask import request
import sqlite3
from flask import flash  # 利用flash 
from app import app

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
            t_id = request.form['variety'] #產品種類
            amount = request.form['amount'] #數量
            price = request.form['price'] #價錢
            origin = request.form['origin'] #產地 
            seller_email = request.form['email'] #會員信箱
            with sqlite3.connect('Database.db') as con :
                cur = con.cursor()
                cur.execute(  #加入新商品資訊 
                    "INSERT INTO product ( seller_email , product_name , type_id , store  , price , origin  ) VALUE( ?,?,?,?,?,?) ", ( seller_email , nm , t_id , amount , price , origin  ) ) 
                con.commit()
                flash('Grouping  Success!') #利用 flash 顯示 開團成功 
        except:
            con.rollback()
            flash('Grouping  ERROR !') #利用 flash 顯示 開團失敗 
        finally:
            con.close()
