menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

->"""

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

def depositar(saldo, valor, extrato,/):
    if valor > 0:

        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"

        return saldo, extrato
    
    else: 
        print("Valor inválido. Tente novamente.")

def sacar(saldo, numero_saques, LIMITE_SAQUES):
    valor = float(input("Digite o valor a ser sacado: "))
    if valor > saldo:
        print("Saldo insuficiente")
        return 0
    elif numero_saques >= LIMITE_SAQUES:
        print("Excedido número de saques diários.")
        return 0
    elif valor > limite:
        print("Valor do saque excede o limite")
        return 0
    elif valor > 0:
        return valor
    else:
        print("Operação falhou. Informe um valor válido para saque")
        return 0
    
 
while True:
    
    opcao = input(menu)

    if opcao == 'd':
        valor = float(input("Digite o valor a ser depositado: "))
        saldo, extrato = depositar(saldo, valor, extrato)

    elif opcao == 's':
        valor_saque = sacar(saldo, numero_saques, LIMITE_SAQUES)
        if valor_saque > 0:
            saldo -= valor_saque
            extrato += f"Saque: R$ {valor_saque:.2f}\n"
            numero_saques += 1 

    elif opcao == "e":
        print("\n============== EXTRATO ==============")
        print(extrato if extrato else "Sem registro de movimentação." )
        print(f"Saldo: R$ {saldo:.2f}")
        print("\n=====================================")
        
    elif opcao == "q":
        break

    else:
        print("Operação inválida. por favor selecione novamente a operação desejada")


