import sqlite3

def criar_tabela_afiliados():
    con = sqlite3.connect("lanchonete.db")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS afiliados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            codigo TEXT,
            afiliador TEXT,
            vendas INTEGER,
            comissao REAL
        )
    """)

    con.commit()
    con.close()
