def main():

    fh = open("matriz.txt", "r")
    #print(fh.read())

    data = fh.readlines()
    matriz = list()
    for line in data:
        listaAux = list()
        for num in line.split():
            listaAux.append(int(num))
        matriz.append(listaAux)

    dibujaMatriz(matriz)


def dibujaMatriz(M):
    for i in range(len(M)):
        for j in range(len(M[i])):
            print(str(M[i][j]) + " ", end='')
        print()


if __name__ == '__main__':
    main()