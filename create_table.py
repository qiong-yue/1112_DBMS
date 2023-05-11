import sqlite3

conn = sqlite3.connect('DB.db')
print("connect successfully")

#可以在這裡建立table 和 data (要在commit()之前完成 )

conn.execute(
    "DROP TABLE user ")
conn.execute(
    "DROP TABLE product " )
conn.execute(
    'CREATE TABLE IF NOT EXISTS product(product_id INTEGER PRIMARY KEY ,seller_id INTEGER ,  name TEXT , type_id INTEGER , amount INTEGER ,release_date TEXT , off_date TEXT ,  price INTEGER , origin TEXT , rating REAL ) ')
conn.execute(
    'CREATE TABLE IF NOT EXISTS user( user_id INTEGER PRIMARY KEY , username TEXT , address TEXT , phone TEXT , Bdate TEXT , email TEXT , password TEXT ) ' )
#conn.execute(
 #   "INSERT INTO product( product_id , seller_id , name , type_id , amount , release_date , off_date , price , origin , rating ) VALUES(?,?,?,?,?,?,?,?,?,?) " , ( 1 , 1 , 'icecream', 1 , 100 , '2023-05-05' , '2023-05-10' , 20 , 'taipei' , 3.9 ))

#conn.execute(
 #   "INSERT INTO user( user_id , username , address , phone , Bdate , email , password ) VALUES(?,?,?,?,?,?,?)" , ( 1 , 'cathy' , 'cheng hun' , '0989531768' ,  '2003-08-27' , 'cathy@gmail.com' , 'cathy0827' ))

conn.commit()
print("add seccessfully")

conn.close()
