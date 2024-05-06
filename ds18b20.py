import time
import onewire
import ds18x20
from machine import Pin
import config

# Configura o pino do DS18B20
ds_pin = Pin(config.DS18B20_PIN)

# Inicializa o barramento OneWire
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

def read_ds18b20():
    # Faz a leitura do sensor DS18B20
    roms = ds_sensor.scan()
    ds_sensor.convert_temp()
    time.sleep_ms(750)  # Aguarda a conversão

    # Obtém a temperatura de cada sensor encontrado
    temperatures = []
    for rom in roms:
        temp = ds_sensor.read_temp(rom)
        if isinstance(temp, float):
            temperatures.append(temp)

    return temperatures
