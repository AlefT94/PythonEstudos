#Crie uma exceção personalizada SaldoInsuficienteError.
class SaldoInsuficienteError(Exception):
    def __init__(self, message = "Saldo insuficiente."):
        self.message = message
        super().__init__(self.message)

def processar_transferencia(origem: dict, destino: dict, valor: float) -> None:
    try:
        if valor <= 0:
            raise ValueError("O valor da transferência deve ser maior que zero.")
        if origem['saldo'] < valor:
            raise SaldoInsuficienteError(f"Saldo insuficiente na conta de origem. Saldo atual: {origem['saldo']}, valor da transferência: {valor}.")
    except (ValueError, SaldoInsuficienteError) as e:
        print(f"Erro ao processar transferência: {e}")
    else:
        origem['saldo'] -= valor
        destino['saldo'] += valor
        print(f"Transferência de {valor} realizada com sucesso. Novo saldo da conta de origem: {origem['saldo']}, novo saldo da conta de destino: {destino['saldo']}.")
    finally:
        print("Processamento da transferência concluído.")