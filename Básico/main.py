#1 Crie uma lista com números de 1 a 20 e gere outra contendo apenas os números pares.

# x = 1
# lista = []

# while x<=20:
#     lista.append(x)
#     x += 1

# print("Lista completa:", lista)

# lista2 = [num for num in lista if num % 2 == 0]
# print("Lista com números pares:", lista2)

# lista3 = []
# for num in lista:
#     if num % 2 == 0:
#         lista3.append(num)

# print("Lista com números pares (método 3):", lista3)

#2 Crie uma função que receba uma lista de preços e retorne o maior, o menor e a média

# def calcular_precos(precos):
#     maior = max(precos)
#     menor = min(precos)
#     media = sum(precos) / len(precos)
#     return maior, menor, media


# maior, menor, media = calcular_precos([10.5, 20.0, 5.75, 15.0, 30.25])
# print(f"Maior preço: {maior}")
# print(f"Menor preço: {menor}")
# print(f"Média preço: {media}")

#3 Dado o texto abaixo, conte quantas palavras diferentes existem:

# texto = "python react python api react python"
# palavras = texto.split(" ")
# dicionario: dict[str, int] = {}

# for palavra in palavras:
#     dicionario[palavra] = dicionario.get(palavra, 0) + 1

# print(f"Quantidade de palavras diferentes: {len(dicionario)}")

#4 Crie uma lista de usuários e filtre aqueles que:

usuarios = [
    {"nome": "Alef", "ativo": True},
    {"nome": "Lisia", "ativo": False},
    {"nome": "Milena", "ativo": True},
    {"nome": "Gustavo"}
]


ativos = [user for user in usuarios if user.get("ativo",True)]

print(ativos)