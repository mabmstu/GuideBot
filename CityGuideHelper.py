import sqlite3

conn = sqlite3.connect("C:\\my_env\\GuideBot\\Overall.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM sight WHERE city ='Уфа'")
data = cursor.fetchall()
print(data)
