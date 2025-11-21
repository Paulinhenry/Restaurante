import sqlite3

con = sqlite3.connect("lanchonete.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS pedidos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    item TEXT,
    conta REAL,
    endereco TEXT
)
""")

con.commit()
con.close()
