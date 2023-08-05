

import concurrent
import time


def saludo(nombre: str) -> None:
    print(f'Hola, {nombre}')

def factorial(number):

    if number == 1 or number == 0:
        return 1

    result = 1

    for x in range(1, number + 1, 1):
        result *= x
    return result

def calculo_paralelo(numero: int):
    inicio = time.time()

    numbers = []
    result_list = []
    res = []
    for i in range(numero, 0, -1):
        numbers.append(i)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        result_list = executor.map(factorial, numbers)

    for result in result_list:
        res.append(result)

    final = time.time()
    print(f' tiempo transcurrido = {final - inicio}')

    return res


def main():
    # help(saludo)
    saludo("Pepe")

if __name__=='__main__':
    main()