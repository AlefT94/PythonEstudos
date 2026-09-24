from servico_usuario import SaldoInsuficienteError 
from servico_usuario import processar_transferencia

if __name__ == "__main__":
    conta_origem = {'nome': 'Alice', 'saldo': 150.0}
    conta_destino = {'nome': 'Bob', 'saldo': 500.0}

    print(f"Saldo inicial da conta de origem: {conta_origem['saldo']}")
    print(f"Saldo inicial da conta de destino: {conta_destino['saldo']}")

    valor_transferencia = 100
    processar_transferencia(conta_origem, conta_destino, valor_transferencia)

    print(f"Saldo final da conta de origem: {conta_origem['saldo']}")
    print(f"Saldo final da conta de destino: {conta_destino['saldo']}")