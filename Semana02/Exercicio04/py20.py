try:
    x = int(input("Digite um número: "))
    y = int(input("Digite outro número: "))
    resultado = x / y
    print("O resultado da divisão é:", resultado)
except ZeroDivisionError:
    print("Não é possível dividir por zero!")
except ValueError:
    print("Digite apenas números inteiros!")