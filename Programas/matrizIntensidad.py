def main():

    archivo = open("matriz.txt", "r")

    data = archivo.readlines()
    matriz = list()
    for line in data:
        listaAux = list()
        for num in line.split():
            listaAux.append(int(num))
        matriz.append(listaAux)

    escribirMatriz(matriz)


def escribirMatriz(M):
    for i in range(len(M)):
        for j in range(len(M[i])):
            print(str(M[i][j]) + " ", end='')
        print()


if __name__ == '__main__':
    main()