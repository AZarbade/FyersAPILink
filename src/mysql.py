import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="noir",
    database="stock_data")

cursor = mysql.cursor()
sql = "INSERT INTO stock_data (symbol, price, timestamp) VALUES (%s, %s, %s)"
values = ("AAPL", 150.25, "2024-02-03 12:00:00")

cursor.execute(sql, values)
db.commit()
