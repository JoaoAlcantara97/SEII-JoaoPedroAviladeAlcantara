nome_arquivo = "meu_arquivo.txt"

# cria um novo arquivo de texto
with open(nome_arquivo, 'w') as arquivo:
    arquivo.write("Olá, mundo!\n")
    arquivo.write("Este é o meu primeiro arquivo de texto.\n")

print(f"O arquivo '{nome_arquivo}' foi criado.")