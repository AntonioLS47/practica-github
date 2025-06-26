
def extraer(nombre_archivo, len_header):
    Temperatura = []
    Humedad = []
    Presion = []
    Hora = []
    Fecha = []
    with open(nombre_archivo, "r") as pfile:
        for line in pfile:
            l += 1
            if l > len_header:
                pass
            for cadena in datos.str:
                valores = cadena.split(',')
                Tiempos = valores[0].split(' ')
                Numeros = []
                for valor in valores[1:]:
                    Numeros.append(float(valor))
                Temperatura.append(Numeros[0])
                Humedad.append(Numeros[1])
                Presion.append(Numeros[2])
                valores = cadena.split(' ')
                for valor in valores:
                    Fecha.append(valores[0])
                    Hora.append(valores[1])
                datos = {
                    'T': Temperatura,
                    'H': Humedad,
                    'P': Presion,
                    'Hora': Hora,
                    'Fecha': Fecha
                }
                return datos
