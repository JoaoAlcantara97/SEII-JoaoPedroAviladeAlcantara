import csv

# define os dados a serem escritos no arquivo CSV
dados = [
    ["Nome", "Idade", "Profissão"],
    ["João", "25", "Desenvolvedor"],
    ["Maria", "30", "Engenheira"],
    ["Pedro", "40", "Analista"]
]

# define o nome do arquivo CSV
nome_arquivo = "meu_arquivo.csv"

# abre o arquivo CSV em modo de escrita
with open(nome_arquivo, mode="w", newline="") as arquivo:
    # cria um objeto escritor CSV
    escritor_csv = csv.writer(arquivo)
    
    # escreve os dados no arquivo CSV
    for linha in dados:
        escritor_csv.writerow(linha)

print(f"Arquivo '{nome_arquivo}' criado com sucesso.")