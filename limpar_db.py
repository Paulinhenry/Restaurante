import sqlite3

con = sqlite3.connect("lanchonete.db")
cur = con.cursor()

cur.execute("DELETE FROM afiliados")
cur.execute("DELETE FROM pedidos")
con.commit()

con.close()

print("Tabela afiliados e pedidos limpa!")
