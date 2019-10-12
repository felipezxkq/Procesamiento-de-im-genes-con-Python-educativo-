import analisisImagen


def reconoce_numero(imagen):
    numero_reconocido = 1
    valor_minimo = analisisImagen.analizar(1, imagen)
    for i in range(2, 16):
        nuevo_valor = analisisImagen.analizar(i, imagen)
        if nuevo_valor < valor_minimo:
            valor_minimo = nuevo_valor
            numero_reconocido = i

    if valor_minimo < 0.1:
        return numero_reconocido
    else:
        return -1  # indica que no se reconoció ningun número