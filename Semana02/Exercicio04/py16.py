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

# abre o arquivo CSV em modo de leitura
with open(nome_arquivo, mode="r") as arquivo:
    # cria um objeto leitor CSV
    leitor_csv = csv.reader(arquivo)
    
    # cria a lista HTML
    lista_html = "<ul>\n"
    
    # itera sobre as linhas do arquivo CSV
    for linha in leitor_csv:
        # adiciona uma nova linha à lista HTML
        lista_html += "  <li>" + " | ".join(linha) + "</li>\n"
    
    lista_html += "</ul>"
    
print(lista_html)