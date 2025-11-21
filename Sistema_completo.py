import sqlite3
from dataclasses import dataclass
import sys


# ==========================================
# 1. CONFIGURAÇÃO E BANCO DE DADOS
# ==========================================

def inicializar_banco():
    """Cria todas as tabelas necessárias se não existirem."""
    con = sqlite3.connect("lanchonete.db")
    cur = con.cursor()

    # Tabela de Pedidos (Baseado em Banco.py)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS pedidos
                (
                    id
                    INTEGER
                    PRIMARY
                    KEY
                    AUTOINCREMENT,
                    nome
                    TEXT,
                    item
                    TEXT,
                    conta
                    REAL,
                    endereco
                    TEXT
                )
                """)

    # Tabela de Afiliados (Baseado em Sistema afiliação.py)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS afiliados
                (
                    id
                    INTEGER
                    PRIMARY
                    KEY
                    AUTOINCREMENT,
                    nome
                    TEXT,
                    codigo
                    TEXT,
                    afiliador
                    TEXT,
                    vendas
                    INTEGER,
                    comissao
                    REAL
                )
                """)

    con.commit()
    con.close()


# ==========================================
# 2. MÓDULO ADMINISTRATIVO (AFILIADOS)
# ==========================================

@dataclass
class Afiliado:
    id: int
    nome: str
    codigo: str
    afiliador: str
    vendas: int
    comissao: float


def menu_admin():
    print("\n=== ÁREA RESTRITA: ADMINISTRADOR ===")
    # Carrega afiliados do banco na memória para manipular
    # (Simplificação para manter sua lógica original)
    afiliados = carregar_afiliados_do_banco()

    while True:
        print("\n--- MENU ADMIN ---")
        print("1 - Cadastrar afiliado")
        print("2 - Registrar venda (Manual)")
        print("3 - Listar afiliados")
        print("4 - Ver indicados")
        print("5 - Salvar e Voltar ao Menu Principal")

        opcao = input("> ")

        if opcao == "1":
            cadastrar_afiliado(afiliados)
        elif opcao == "2":
            registrar_venda_manual(afiliados)
        elif opcao == "3":
            listar_afiliados(afiliados)
        elif opcao == "4":
            ver_indicados(afiliados)
        elif opcao == "5":
            # Salva tudo antes de sair
            for af in afiliados:
                salvar_afiliado_no_banco(af)
            break
        else:
            print("Opção inválida!")


def carregar_afiliados_do_banco():
    """Carrega os dados do banco para a lista de objetos"""
    lista = []
    con = sqlite3.connect("lanchonete.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM afiliados")
    dados = cur.fetchall()
    con.close()

    for linha in dados:
        # linha: id, nome, codigo, afiliador, vendas, comissao
        novo = Afiliado(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5])
        lista.append(novo)
    return lista


def salvar_afiliado_no_banco(af):
    con = sqlite3.connect("lanchonete.db")
    cur = con.cursor()

    # Verifica se já existe para atualizar ou inserir (Upsert simples)
    cur.execute("SELECT id FROM afiliados WHERE id = ?", (af.id,))
    existe = cur.fetchone()

    if existe:
        cur.execute("""
                    UPDATE afiliados
                    SET vendas   = ?,
                        comissao = ?
                    WHERE id = ?
                    """, (af.vendas, af.comissao, af.id))
    else:
        cur.execute("""
                    INSERT INTO afiliados (nome, codigo, afiliador, vendas, comissao)
                    VALUES (?, ?, ?, ?, ?)
                    """, (af.nome, af.codigo, af.afiliador, af.vendas, af.comissao))

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
    salvar_afiliado_no_banco(novo)  # Salva imediatamente
    print("Afiliado cadastrado!\n")


def registrar_venda_manual(afiliados):
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
        print(f"ID: {af.id} | Nome: {af.nome} | Cód: {af.codigo} | Vendas: {af.vendas} | Com: R${af.comissao:.2f}")


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


# ==========================================
# 3. MÓDULO CLIENTE (CARDÁPIO E PEDIDOS)
# ==========================================

def salvar_pedido_banco(nome, item, conta, endereco):
    con = sqlite3.connect("lanchonete.db")
    cur = con.cursor()
    cur.execute("""
                INSERT INTO pedidos (nome, item, conta, endereco)
                VALUES (?, ?, ?, ?)
                """, (nome, item, conta, endereco))
    con.commit()
    con.close()


def executar_pedidos():
    print("\n=== BEM-VINDO À LANCHONETE ===")
    endereco_loja = "Rua Cristovão"
    itens_pedidos = []
    i = 1
    conta = 0

    while True:
        valor = 0
        item = ""

        print("\nAqui está o cardápio: ")
        print("1 --> X-burguer 14R$")
        print("2 --> X-salada 16R$")
        print("3 --> X-bacon 18R$")
        print("4 --> X-tudo 20R$")
        print("O que você deseja ???")

        try:
            opcao = int(input("> "))
        except ValueError:
            print("Por favor, digite apenas números.")
            continue

        if opcao not in [1, 2, 3, 4]:
            print("ERROR: ITEM NÃO DISPONIVEL NO CARDAPIO")
        else:
            match opcao:
                case 1:
                    valor = 14
                    item = "X-burguer"
                case 2:
                    valor = 16
                    item = "X-salada"
                case 3:
                    valor = 18
                    item = "X-bacon"
                case 4:
                    valor = 20
                    item = "X-tudo"

            print(f"Anotado!!! o {i}° item escolhido foi {item} e possui o valor de {valor} R$ ")
            conta += valor
            itens_pedidos.append(item)
            i += 1

        print("Deseja algo a mais ??? (S/N)")
        algo_mais = input().upper()
        if algo_mais != "S" and algo_mais != "Y":
            break

    print(f"A conta total deu {conta} R$")
    print("Digite o Nome associado ao pedido")
    nome = input()

    print("Irá ser para entrega ??? (S/N)")
    entrega = input().upper()

    endereco_final = ""
    if entrega in ("S", "Y"):
        print("Digite o nome da Rua/Avenida")
        rua = input()
        print("Digite o número")
        numero = input()
        print("Digite o ponto de referencia (opcional)")
        ponto_ref = input()

        if ponto_ref != "":
            endereco_final = f"{rua}, {numero}, {ponto_ref}"
        else:
            endereco_final = f"{rua}, {numero}"
        print(f"Entrega: {endereco_final}")
    else:
        endereco_final = f"Retirada na loja ({endereco_loja})"
        print(endereco_final)

    itens_str = ", ".join(itens_pedidos)
    salvar_pedido_banco(nome, itens_str, conta, endereco_final)
    print(f"Obrigado pela preferência {nome}, volte sempre !!!")
    input("\nPressione ENTER para voltar ao menu principal...")


# ==========================================
# 4. MENU PRINCIPAL (MAIN)
# ==========================================

def main():
    inicializar_banco()

    while True:
        print("\n" + "=" * 30)
        print("   SISTEMA CENTRAL LANCHONETE")
        print("=" * 30)
        print("1 - Novo Pedido (Cliente)")
        print("2 - Acesso Administrativo (Afiliados)")
        print("3 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            executar_pedidos()
        elif opcao == "2":
            senha = input("Digite a senha de admin (padrão: admin): ")
            if senha == "admin":
                menu_admin()
            else:
                print("Senha incorreta!")
        elif opcao == "3":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()