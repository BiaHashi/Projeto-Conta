from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Pessoa_Fisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta_Bancaria:
    def __init__(self, numero, cliente):
        self.__saldo = 0
        self.__numero = numero
        self.__cliente = cliente
        self.__agencia = '0001'
        self.__historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self.__saldo
    
    @property
    def numero(self):
        return self.__numero
    
    @property
    def cliente(self):
        return self.__cliente
    
    @property
    def agencia(self):
        return self.__agencia
    
    @property
    def historico(self):
        return self.__historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo o suficiente. @@@")
        elif valor > 0:
            self.__saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n§§§ Operação falhou! O valor que informou é inválido. §§§")
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            print("\n$$$ Depósito realizado com sucesso! $$$")
        else:
            print("\n*** Operação falhou! O valor informado é inválido. ***")
            return False
        return True

class Conta_Corrente(Conta_Bancaria):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['Tipo'] == Saque.__name__]
        )
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limites_saques
        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n§§§ Operação falhou! Número máximo de saques excedido. §§§")
        else:
            return super().sacar(valor)
        return False
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self.transacoes = []

    @property
    def transacoes(self):
        return self.__transacoes

    def adicionar_transacao(self, transacao):
        self.__transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now().strftime("%d-%m-%Y %H:%M%S")
            }
        )

class Transacao(ABC):
    @property
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self.__valor = valor

    @property
    def valor(self):
        return self.__valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        
class Deposito(Transacao):
    def __init__(self, valor):
        self.__valor = valor

    @property
    def valor(self):
        return self.__valor
    
    def register(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Conta
    [lc]\tListar Contas
    [nu]\tNovo Usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_corrente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return 
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado.")
        return
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_corrente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado.")
        return
    valor = float(input("Informe o valor do saque"))
    transacao = Saque(valor)
    conta = recuperar_conta_corrente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado.")
        return
    conta = recuperar_conta_corrente(cliente)
    if not conta:
        return
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo:\n\t{conta.saldo:.2f}")
    print("==========================================")

def criar_cliente(clientes):
    cpf = input("Informe seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("\nJá existe um cliente com esse CPF")
        return
    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimeto completo (DD/MM/AAAA): ")
    endereco = input("Informe seu endereço completo: ")
    cliente = Pessoa_Fisica(nome = nome, data_nascimento = data_nascimento, cpf = cpf, endereco = endereco)
    clientes.append(cliente)
    print("\n\tCliente criado com sucesso!!")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado, fluxo de criação encerrado.")
        return
    conta = Conta_Corrente.nova_conta(cliente = cliente, numero = numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print("\nConta criada com sucesso!!!")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []
    while True:

        opcao = menu()
        
        if opcao == 'd':
            depositar(clientes)
        
        elif opcao == 's':
            sacar(clientes)
        
        elif opcao == 'e':
            exibir_extrato(clientes)
        
        elif opcao == 'nu':
            criar_cliente(clientes)
        
        elif opcao == 'nc':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        
        elif opcao == 'lc':
            listar_contas(contas)
        
        elif opcao == 'q':
            break
        
        else:
            print("\nOperação inválida, por favor, seleciona novamente a operação desejada.")

main()