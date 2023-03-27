import os

# retorna o diretório atual
dir_atual = os.getcwd()
print(f"O diretório atual é: {dir_atual}")

# cria uma nova pasta
nova_pasta = "Minha nova pasta"
os.mkdir(nova_pasta)
print(f"A pasta '{nova_pasta}' foi criada.")

# lista os arquivos no diretório atual
arquivos = os.listdir()
print("Arquivos no diretório atual:")
for arquivo in arquivos:
    print(arquivo)

# remove a pasta criada anteriormente
os.rmdir(nova_pasta)
print(f"A pasta '{nova_pasta}' foi removida.")