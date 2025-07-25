
from machine import Pin, I2C, RTC, SDCard
import os, vfs, time
import bme280
import network
import espnow

# rtc
rtc = RTC()
rtc.datetime((2025, 7, 1, 1, 3, 31, 30, 0))

# Intentar montar SD
try:
    sd = SDCard(slot=2)
    vfs.mount(sd, '/sd')
    ruta_archivo = '/sd/registro.txt'
    sd_ok = True
    print("MicroSD montada correctamente.")
except:
    ruta_archivo = '/flash/registro.txt'
    sd_ok = False
    print("Error al montar microSD. Usando memoria interna.")

# ESP-NOW
sta = network.WLAN(network.STA_IF)
sta.active(True)

e = espnow.ESPNow()
e.active(True)
peer = b'\xbb\xbb\xbb\xbb\xbb\xbb'  # Dirección MAC del receptor
e.add_peer(peer)
e.send(peer, "Starting...")

# I2C y sensor BME280
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
bme = bme280.BME280(i2c=i2c)

# Bucle principal
while True:
    temperature, pressure, humidity = bme.read_compensated_data()
    sht_values = bme.values
    fecha = rtc.datetime()

    cadena = "{:04}/{:02}/{:02} {:02}:{:02}:{:02},{},{},{}".format(
        fecha[0], fecha[1], fecha[2], fecha[4], fecha[5], fecha[6],
        sht_values[0], sht_values[1], sht_values[2]
    )

    print(cadena)
    e.send(peer, cadena)

    # Guardar en archivo
    try:
        with open(ruta_archivo, 'a') as f:
            print(cadena, file=f)
    except Exception as err:
        print("Error al guardar:", err)

    time.sleep(2)
