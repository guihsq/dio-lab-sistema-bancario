from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

class Transacao(ABC):

    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Cliente:
    
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)
    
    @property
    def endereco(self):
        return self._endereco
    
    @property
    def contas(self):
        return self._contas
        
class PessoaFisica(Cliente):

    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def nome(self):
        return self._nome
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def data_nascimento(self):
        return self._data_nascimento

class Conta:

    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print("Saldo insuficiente")
        
        elif valor > 0:
            self._saldo -= valor
            print(f"Saque de R$ {valor:.2f} realizado com sucesso ")
            return True
        
        else:
            print("Operação falhou. Informe um valor válido para saque")
        
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso ")
            return True
        
        else: 
            print("Valor inválido. Tente novamente.")    
        
        return False
    
class ContaCorrente(Conta):

    def __init__(self, numero, cliente, limite=500, limite_saques=3, limite_transacoes=10):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.limite_transacoes = limite_transacoes

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        numero_transacoes = len(self.historico.transacoes_do_dia())
        excedeu_limite = valor >= self.limite
        excedeu_saques = numero_saques >= self.limite_saques
        excedeu_transacoes = numero_transacoes >= self.limite_transacoes
        
        if excedeu_limite:
            print("Valor do saque excede o limite")
        elif excedeu_saques:
            print("Excedido número de saques diários.")
        elif excedeu_transacoes:
            print("Excedido número de transações")
        else:
            return super().sacar(valor)

        return False
    
    def depositar(self, valor):
        numero_transacoes = len(self.historico.transacoes_do_dia())
        
        excedeu_transacoes = numero_transacoes >= self.limite_transacoes

        if excedeu_transacoes:
            print("Excedido número de transações")
        else:
            return super().depositar(valor)

        return False
    
    def __str__(self):
        return f"\nAgência: {self._agencia} \nC/C: {self._numero} \nTitular: {self._cliente.nome}"
    
class Historico:
    
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
            return self._transacoes
        
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )
    def transacoes_do_dia(self):
        transacoes_filtradas = []

        for transacao in self.transacoes:
            dttransacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S")
            if abs(dttransacao - datetime.now()).days == 0:
                transacoes_filtradas.append(transacao)
        
        return transacoes_filtradas

def filtrar_cliente(cpf, clientes):
    
    clientes_filtrados=[]

    for cliente in clientes:
        if cliente.cpf == cpf:
            clientes_filtrados.append(cliente)

    if clientes_filtrados:
        return clientes_filtrados[0]
    else:
        return None
    
def filtrar_conta(numero_conta, cliente):
    
    conta = next((conta for conta in cliente.contas if conta.numero == numero_conta), None)
    if conta is None:
        print("Conta não encontrada.")
        return
    
    return conta 

def recuperar_conta_cliente(cliente):
    
    if not cliente.contas:
        print("Cliente não possui conta cadastrada")
        return
    elif len(cliente.contas) == 1:
        return cliente.contas[0]
    else:
        for conta in cliente.contas:
            print(f"Numero Conta: {conta.numero} Cliente: {conta.cliente.nome}")
        numero_conta = int(input("Informe o número da conta deseja operar: "))

        return filtrar_conta(numero_conta, cliente)
        
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    valor = float(input("Informe o valor a ser depositado: "))

    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    valor = float(input("Informe o valor a ser sacado: "))

    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def cadastrar_cliente(clientes):
    cpf = input("CPF (somente números): ")

    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Cliente já cadastrado")
        return
    
    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(endereco, cpf, nome, nascimento)

    clientes.append(cliente)

    print("Cliente cadastrado com sucesso")

def cadastrar_conta(nro_conta, clientes, contas):
    cpf = input("CPF (somente números): ")

    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não econtrado")
        return
    
    conta = ContaCorrente.nova_conta(cliente, nro_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta cadastrada com sucesso")

def imprimir_extrato(clientes):
    cpf = input("Informe o CPF do cliente")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    conta = recuperar_conta_cliente(cliente)
    
    print("\n============== EXTRATO ==============")
    transacoes = conta.historico.transacoes

    extrato =""

    if not transacoes:
        extrato = "Não há movimentação para ser exibida"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao["data"]} {transacao["tipo"]}: R$ {transacao["valor"]:.2f}"
    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("\n=====================================")

def listar_contas(contas):
    for conta in contas:
        print(str(conta))

def menu():
    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [c] Cadastrar Cliente
    [cc] Cadastrar Conta
    [lc] Listar Contas
    [q] Sair

    ->"""

    return menu

def main():

    clientes = []
    contas = []
    
    while True:
        
        opcao = input(menu())

        if opcao == 'd':
            depositar(clientes)

        elif opcao == 's':
            sacar(clientes)

        elif opcao == "e":
            imprimir_extrato(clientes)

        elif opcao == "c":
            cadastrar_cliente(clientes)
            
        elif opcao == "cc":
            
            nro_conta = len(contas)+1
            cadastrar_conta(nro_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida. por favor selecione novamente a operação desejada")

main()