pessoas = [("João", 30), ("Maria", 25), ("Pedro", 40)]
relacionamentos = [("João", "Maria"), ("Maria", "Pedro")]

for pessoa in pessoas:
    nome = pessoa[0]
    idade = pessoa[1]
    parceiro = ""
    for rel in relacionamentos:
        if rel[0] == nome:
            parceiro = rel[1]
            break
    print(f"{nome} ({idade} anos) é casado com {parceiro}.")