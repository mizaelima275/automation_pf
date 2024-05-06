# Configurações Wi-Fi
WIFI_SSID = "******"
WIFI_PASSWORD = "******"

# Configurações MQTT
MQTT_BROKER = "******"
MQTT_PORT = 1883
MQTT_USER = "******"
MQTT_PASSWORD = "******"
CLIENT_ID = "esp32_delefaz"

# TÓPICOS MQTT DE COMANDO
COMMAND_TOPIC_EVAPORADORA = "delefaz/command/evaporadora"
COMMAND_TOPIC_CICLO1 = "delefaz/command/ciclo1"
COMMAND_TOPIC_CICLO2 = "delefaz/command/ciclo2"
COMMAND_AUTOMATION = "delefaz/command/automation"

# TÓPICOS MQTT DE STATUS
STATE_TOPIC_EVAPORADORA = "delefaz/status/evaporadora"
STATE_TOPIC_CICLO1 = "delefaz/status/ciclo1"
STATE_TOPIC_CICLO2 = "delefaz/status/ciclo2"
TEMPERATURA_TOPIC = "delefaz/status/sensor"
TEMPERATURA_SETPOINT = "delefaz/setpoint"

# Configurações GPIO
GPIO_EVAPORADORA = 27
GPIO_CICLO1 = 26
GPIO_CICLO2 = 25
DS18B20_PIN = 14

# Variáveis globais
histerese = float(1.8)
diferencial = float(1.5)