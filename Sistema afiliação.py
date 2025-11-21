from dataclasses import dataclass
import sqlite3
@dataclass
class Afiliado:
    id: int
    nome: str
    codigo: str
    afiliador: str
    vendas: int
    comissao: float
afiliados = []

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

def cadastrar_afiliado(afiliados):
    print("Nome do afiliado:")
    nome = input()

    print("Código do afiliado:")
    codigo = input()

    print("Código de quem indicou:")
    afiliador = input()

    novo = Afiliado(
        id=len(afiliados) + 1,
        nome=nome,
        codigo=codigo,
        afiliador=afiliador,
        vendas=0,
        comissao=0.0
    )
    afiliados.append(novo)
    print("Afiliado cadastrado!\n")

def registrar_venda(afiliados):
    print("Código do afiliado:")
    codigo = input("> ")
    for af in afiliados:
        if af.codigo == codigo:
            print("Valor da venda:")
            valor = float(input("> "))

            af.vendas += 1
            af.comissao += valor * 0.10

            print("Venda registrada!\n")
            return

    print("Afiliado não encontrado!\n")

def listar_afiliados(afiliados):
    print("\n--- LISTA DE AFILIADOS ---")
    for af in afiliados:
        print(f"ID: {af.id} | Nome: {af.nome} | Código: {af.codigo} | Afiliador: {af.afiliador} | Vendas: {af.vendas} | Comissão: R${af.comissao}")
    print()
def ver_indicados(afiliados):
    print("Código do afiliador:")
    codigo = input("> ")

    print(f"\nIndicados por {codigo}:")
    achou = False
    for af in afiliados:
        if af.afiliador == codigo:
            print(f"- {af.nome} ({af.codigo})")
            achou = True

    if not achou:
        print("Nenhum indicado encontrado.\n")

def salvar_no_banco(af):
    con = sqlite3.connect("lanchonete.db")
    cur = con.cursor()

    cur.execute("""
        INSERT INTO afiliados (nome, codigo, afiliador, vendas, comissao)
        VALUES (?, ?, ?, ?, ?)
    """, (af.nome, af.codigo, af.afiliador, af.vendas, af.comissao))

    con.commit()
    con.close()

def main():
    criar_tabela_afiliados()  # ← criar tabela se não existir

    afiliados = []

    while True:
        print("=== MENU ===")
        print("1 - Cadastrar afiliado")
        print("2 - Registrar venda")
        print("3 - Listar afiliados")
        print("4 - Ver indicados")
        print("5 - Salvar no banco de dados")
        print("6 - Sair")

        opcao = input("> ")

        if opcao == "1":
            cadastrar_afiliado(afiliados)
        elif opcao == "2":
            registrar_venda(afiliados)
        elif opcao == "3":
            listar_afiliados(afiliados)
        elif opcao == "4":
            ver_indicados(afiliados)
        elif opcao == "5":
            for af in afiliados:
                salvar_no_banco(af)
        elif opcao == ("6"):
            break
        else:
            print("Opção inválida!\n")

main()


