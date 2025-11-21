import sqlite3

con = sqlite3.connect("lanchonete.db")
cur = con.cursor()

cur.execute("SELECT * FROM pedidos")
dados = cur.fetchall()

for linha in dados:
    print(linha)

con.close()
