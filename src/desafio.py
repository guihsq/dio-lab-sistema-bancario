
def menu():
    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [c] Cadastrar Cliente
    [q] Sair

    ->"""

    return menu

def cadastrar_cliente(clientes, cliente):
     clientes.append(cliente)
     print("Cliente cadastrado com sucesso!")
     return clientes

def depositar(saldo, valor, extrato,/):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso ")
    else: 
        print("Valor inválido. Tente novamente.")
    
    return saldo, extrato

def sacar(*,saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES):
    
    if valor > saldo:
        print("Saldo insuficiente")
    elif numero_saques >= LIMITE_SAQUES:
        print("Excedido número de saques diários.")
    elif valor > limite:
        print("Valor do saque excede o limite")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso ")
    else:
        print("Operação falhou. Informe um valor válido para saque")

    return saldo, extrato, numero_saques   

def imprimir_extrato(saldo,/,*, extrato):
    print("\n============== EXTRATO ==============")
    print(extrato if extrato else "Sem registro de movimentação." )
    print(f"Saldo: R$ {saldo:.2f}")
    print("\n=====================================")

def filtrar_cliente(cpf, clientes):
    
    clientes_filtrados=[]

    for cliente in clientes:
        if cliente["cpf"] == cpf:
            clientes_filtrados.append(cliente)

    if clientes_filtrados:
        return clientes_filtrados[0]
    else:
        return None

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    clientes = []
    
    while True:
        
        opcao = input(menu())

        if opcao == 'd':
            valor = float(input("Digite o valor a ser depositado: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == 's':

            valor = float(input("Digite o valor a ser sacado: "))
            saldo, extrato, numero_saques = sacar(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, LIMITE_SAQUES=LIMITE_SAQUES)

        elif opcao == "e":
            imprimir_extrato(saldo, extrato=extrato)

        elif opcao == "c":
            
            cpf = input("CPF (somente números): ")

            cliente = filtrar_cliente(cpf, clientes)

            if cliente:
                print("Cliente já cadastrado")
            else:
                nome = input("Nome completo: ")
                nascimento = input("Data de nascimento (dd-mm-aaaa): ")
                endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

                cliente = {
                    "cpf": cpf,
                    "nome": nome,
                    "nascimento": nascimento,
                    "endereco": endereco
                }

                clientes = cadastrar_cliente(clientes, cliente)

        elif opcao == "q":
            break

        else:
            print("Operação inválida. por favor selecione novamente a operação desejada")

main()