import sqlite3

# 連到資料庫
conn = sqlite3.connect('DB.db')
print("Connected successfully")

conn.execute(
    "DROP TABLE product ")
conn.execute(
    "DROP TABLE orders " )
conn.execute('CREATE TABLE product (product_id INTEGER PRIMARY KEY, seller_id INTEGER, name TEXT, type_id INTEGER, amount INTEGER, price INTEGER, origin TEXT, rating REAL)')
conn.execute('CREATE TABLE orders (order_id INTEGER PRIMARY KEY, date TEXT, product_id INTEGER, price INTEGER, amount INTEGER, coupon_status INTEGER, located_id INTEGER)')

print("Create successfully")

conn.commit()
conn.close()