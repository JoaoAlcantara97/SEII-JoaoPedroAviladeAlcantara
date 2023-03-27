import datetime

# obtém a data e hora atual
data_atual = datetime.datetime.now()

# imprime a data e hora atual formatada
print("Data e hora atual:", data_atual.strftime("%d/%m/%Y %H:%M:%S"))

# adiciona 1 dia à data atual
data_futura = data_atual + datetime.timedelta(days=1)

# imprime a data futura formatada
print("Data futura:", data_futura.strftime("%d/%m/%Y"))