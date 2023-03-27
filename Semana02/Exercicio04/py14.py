import os

# define o caminho absoluto para a pasta atual
caminho_atual = os.path.abspath(os.getcwd())

# exibe o caminho absoluto para a pasta atual
print(f"Caminho absoluto para a pasta atual: {caminho_atual}")

# lista os arquivos na pasta atual
arquivos = os.listdir()
print("Arquivos na pasta atual:")
for arquivo in arquivos:
    print(arquivo)

# cria uma nova pasta dentro da pasta atual
nova_pasta = "minha_nova_pasta"
caminho_nova_pasta = os.path.join(caminho_atual, nova_pasta)
os.mkdir(caminho_nova_pasta)
print(f"Pasta '{nova_pasta}' criada com sucesso.")

# move um arquivo para a nova pasta
nome_arquivo = "meu_arquivo.txt"
caminho_arquivo = os.path.join(caminho_atual, nome_arquivo)
os.rename(caminho_arquivo, os.path.join(caminho_nova_pasta, nome_arquivo))
print(f"Arquivo '{nome_arquivo}' movido para a pasta '{nova_pasta}'.")

# remove a nova pasta
os.rmdir(caminho_nova_pasta)
print(f"Pasta '{nova_pasta}' removida com sucesso.")