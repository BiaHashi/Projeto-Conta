class Conta_Bancaria:
    def __init__(self, numero, titular, saldo = 0):
        self.numero = numero
        self.titular = titular
        self.saldo = saldo

    def depositar(self, valor):
        self.saldo += valor
        print("Depositando...")
        print(self.saldo)
        
    def sacar(self, saque):
        if saque <= self.saldo:
            self.saldo -= saque
            print("Sacando...")
            print(self.saldo)
        else:
            print("Não foi possível sacar esse valor, tente novamente.")

class Banco:
    def __init__(self):
        self.contas = []

    def criar_conta(self, conta):
        self.contas.append(conta)
    
    def buscar_conta(self, numero):
        for conta in self.contas:
            if conta.numero == numero:
                return conta
        return None
    
    def transferir_valores(self, numero_origem, numero_destino, valor):
        origem = self.buscar_conta(numero_origem)
        destino = self.buscar_conta(numero_destino)
        if origem and destino and origem.saldo >= valor:
            origem.saldo -= valor
            destino.saldo += valor
            print(f"\nTransferência realizada. Você está com {origem.saldo}")
        else:
            print("Ocorreu um erro com a sua transferência. Tente novamente.")
        
        
banco = Banco()
conta1 = Conta_Bancaria(1, "Pedro")
conta2 = Conta_Bancaria(2, "Maria", 250)
banco.criar_conta(conta1)
banco.criar_conta(conta2)
banco.transferir_valores(2, 1, 44)