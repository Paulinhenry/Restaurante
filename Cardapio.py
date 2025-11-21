from unicodedata import numeric
endereco_loja = "Rua Cristovão"
import sqlite3

def salvar_pedido(nome, item, conta, endereco):
    con = sqlite3.connect("lanchonete.db")
    cur = con.cursor()

    cur.execute("""
        INSERT INTO pedidos (nome, item, conta, endereco)
        VALUES (?, ?, ?, ?)
    """, (nome, item, conta, endereco))

    con.commit()
    con.close()
itens_pedidos = []
i = 1
conta = 0
def novo_pedido():
    valor = 0
    item = ""
    algo_mais = ""
    print("Aqui está o cardapio: ")
    print("1 --> X-burguer 14R$")
    print("2 --> X-salada 16R$")
    print("3 --> X-bacon 18R$")
    print("4 --> X-tudo 20R$")
    print("Oque você deseja ???")
    opcao = int(input())
    if (opcao != 1) and (opcao != 2) and (opcao != 3) and (opcao != 4):
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
        print("Anotado!!! o {}° item escolhido foi {} e possui o valor de {} R$ ".format(i,item, valor))
        return valor, item
valor, item = novo_pedido()
conta += valor
itens_pedidos.append(item)
print("Deseja algo a mais ??? (S/N), (Y/N)")
algo_mais = str(input())
while (algo_mais == "S") or (algo_mais == "Y"):
    i = i + 1
    valor, item = novo_pedido()
    conta += valor
    itens_pedidos.append(item)
    print("Deseja algo a mais ??? (S/N), (Y/N)")
    algo_mais = str(input())
print("A conta total deu {} R$".format(conta))
print("Digite o Nome associado ao pedido")
nome = str(input())
print("Irá ser para entrega ??? (S/N), (Y/N)")
entrega = str(input())

if entrega in ("S", "Y"):
    print("Digite o Endereço de Entrega:")
    print("Digite o nome da Rua/Avenida")
    rua = str(input())
    print("Digite o número da casa/apartamento")
    numero = str(input())  # deixei string para evitar problemas
    print("Digite o ponto de referencia (opcional)")
    ponto_ref = str(input())

    if ponto_ref != "":
        endereco_final = f"{rua}, {numero}, {ponto_ref}"
        print(f"Entrega: {endereco_final}")
    else:
        endereco_final = f"{rua}, {numero}"
        print(f"Entrega: {endereco_final}")

else:
    endereco_final = f"Retirada na loja ({endereco_loja})"
    print(endereco_final)

# transformar lista de itens em string
itens_str = ", ".join(itens_pedidos)

# salvar no banco
salvar_pedido(nome, itens_str, conta, endereco_final)

print("Obrigado pela preferência {} volte sempre !!!".format(nome))

