import time
from umqtt.simple import MQTTClient
from machine import Timer  # Importe o módulo Timer
import network
import machine
import config
import ds18b20
import json

gpio_evaporadora = machine.Pin(config.GPIO_EVAPORADORA, machine.Pin.OUT)
gpio_ciclo1 = machine.Pin(config.GPIO_CICLO1, machine.Pin.OUT)
gpio_ciclo2 = machine.Pin(config.GPIO_CICLO2, machine.Pin.OUT)

gpio_evaporadora.value(1)
gpio_ciclo1.value(1)
gpio_ciclo2.value(1)

automation = None
setpoint = 25

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando ao WiFi...")
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print("Conectado ao WiFi:", config.WIFI_SSID)
    
def mqtt_callback(topic, msg):
    global automation
    global setpoint

    topic = topic.decode('utf-8')  # Convertendo bytes para string
    msg = msg.decode('utf-8')  # Convertendo bytes para string
    setpoint = 25

    if msg is not None:  # Verifica se a mensagem não é None
        if topic == config.COMMAND_AUTOMATION:
            automation = msg
            print("Automação:", automation)

        if topic == config.TEMPERATURA_SETPOINT:
            setpoint = float(msg)
            print("Setpoint:", setpoint)

    if automation == "1":
        # Modo manual
        if topic == config.TEMPERATURA_SETPOINT:
            return  # Ignora as mensagens recebidas no tópico

        if topic == config.COMMAND_TOPIC_EVAPORADORA:
            if msg == "0":  # Comparando com string
                gpio_evaporadora.value(0)
            elif msg == "1":  # Comparando com string
                gpio_evaporadora.value(1)

        if topic == config.COMMAND_TOPIC_CICLO1:
            if msg == "0":  # Comparando com string
                gpio_ciclo1.value(0)
            elif msg == "1":  # Comparando com string
                gpio_ciclo1.value(1)

        if topic == config.COMMAND_TOPIC_CICLO2:
            if msg == "0":  # Comparando com string
                gpio_ciclo2.value(0)
            elif msg == "1":  # Comparando com string
                gpio_ciclo2.value(1)

    else:
        # Modo automático
        if topic == config.COMMAND_TOPIC_EVAPORADORA:
            return  # Ignora as mensagens recebidas no tópico

        if topic == config.COMMAND_TOPIC_CICLO1:
            return  # Ignora as mensagens recebidas no tópico

        if topic == config.COMMAND_TOPIC_CICLO2:
            return  # Ignora as mensagens recebidas no tópico

        temperaturas = ds18b20.read_ds18b20()
        if temperaturas:
            temperatura_atual = float(temperaturas[0])

            if temperatura_atual >= setpoint + config.histerese + config.diferencial:
                gpio_evaporadora.value(0)
                gpio_ciclo1.value(0)
                gpio_ciclo2.value(0)
                print("ciclo 2 ativado")
            elif temperatura_atual >= setpoint + config.histerese:
                gpio_evaporadora.value(0)
                gpio_ciclo1.value(0)
                gpio_ciclo2.value(1)
                print("ciclo 1 ativado")
            elif temperatura_atual <= setpoint:
                gpio_evaporadora.value(0)
                gpio_ciclo1.value(1)
                gpio_ciclo2.value(1)
                print("Apenas evaporadora em funcionamento")
               
def connect_mqtt():
    global mqtt_client
    mqtt_client = MQTTClient(config.CLIENT_ID, config.MQTT_BROKER, port=config.MQTT_PORT, user=config.MQTT_USER, password=config.MQTT_PASSWORD)
    mqtt_client.set_callback(mqtt_callback)
    mqtt_client.connect()
    print("Conectado ao Broker MQTT")

    mqtt_client.subscribe(config.COMMAND_TOPIC_EVAPORADORA)
    mqtt_client.subscribe(config.COMMAND_TOPIC_CICLO1)
    mqtt_client.subscribe(config.COMMAND_TOPIC_CICLO2)
    mqtt_client.subscribe(config.TEMPERATURA_SETPOINT)
    mqtt_client.subscribe(config.COMMAND_AUTOMATION)

    print("Subscrito ao tópico:", config.COMMAND_TOPIC_EVAPORADORA)
    print("Subscrito ao tópico:", config.COMMAND_TOPIC_CICLO1)
    print("Subscrito ao tópico:", config.COMMAND_TOPIC_CICLO2)
    print("Subscrito ao tópico:", config.TEMPERATURA_SETPOINT)
    print("Subscrito ao tópico:", config.COMMAND_AUTOMATION)

def publish_status(timer):  
    gpio_evaporadora_state = gpio_evaporadora.value()
    gpio_ciclo1_state = gpio_ciclo1.value()
    gpio_ciclo2_state = gpio_ciclo2.value()

    mqtt_client.publish(config.STATE_TOPIC_EVAPORADORA, str(gpio_evaporadora_state))
    mqtt_client.publish(config.STATE_TOPIC_CICLO1, str(gpio_ciclo1_state))
    mqtt_client.publish(config.STATE_TOPIC_CICLO2, str(gpio_ciclo2_state))

     # Lendo a temperatura
    temperaturas = ds18b20.read_ds18b20()
    if temperaturas:
        temperatura = temperaturas[0] 
        # Formatação da temperatura com uma casa decimal
        temperatura_str = "{:.1f}".format(temperatura)
        # Criando um dicionário com a temperatura
        temperatura_dict = {
            "temperatura": temperatura_str
        }

        # Convertendo o dicionário em uma string JSON
        json_temperatura = json.dumps(temperatura_dict)

        # Publicando a temperatura como uma string JSON
        mqtt_client.publish(config.TEMPERATURA_TOPIC, json_temperatura)
        
def main():
    connect_wifi()
    connect_mqtt()

    # Configurando o temporizador para chamar a função publish_status a cada 5 segundos
    timer = Timer(-1)
    timer.init(period=1000, mode=Timer.PERIODIC, callback=publish_status)

    while True:
        mqtt_client.check_msg()
        time.sleep(1)

if __name__ == "__main__":
    main()