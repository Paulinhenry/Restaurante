from unicodedata import numeric
endereco_loja = "Rua Cristovão"
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
        return valor
valor = novo_pedido()
conta += valor
print("Deseja algo a mais ??? (S/N), (Y/N)")
algo_mais = str(input())
while (algo_mais == "S") or (algo_mais == "Y"):
    i = i + 1
    valor = novo_pedido()
    conta += valor
    print("Deseja algo a mais ??? (S/N), (Y/N)")
    algo_mais = str(input())
print("A conta total deu {} R$".format(conta))
print("Digite o Nome associado ao pedido")
nome = str(input())
print("Irá ser para entrega ??? (S/N), (Y/N)")
entrega = str(input())
if entrega in ("S", "Y"):
    print("Digite o Endereço de Entrega:")
    endereco = []
    print("Digite o nome da Rua/Avenida")
    rua = str(input())
    print("Digite o número da casa/apartamento")
    numero = int(input())
    print("Digite o ponto de referencia (opcional)")
    ponto_ref= str(input())
    endereco.append(rua)
    endereco.append(numero)
    if ponto_ref != "":
        endereco.append(ponto_ref)
        print("Entrega: {}, {}, {}".format(endereco[0], endereco[1], endereco[2]))
    else:
        print("Entrega: {}, {}".format(endereco[0], endereco[1]))
else:
    print("OK!!! Pode retirar no endereço {}".format(endereco_loja))

print("Obrigado pela preferência {} volte sempre !!!".format(nome))

