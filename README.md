# Projeto de Controle de Climatização

Este projeto implementa um sistema de controle de climatização utilizando um microcontrolador ESP32 e comunicação MQTT para monitorar e controlar dispositivos como evaporadora e ciclos de refrigeração em um ambiente. O objetivo é permitir tanto o controle manual quanto o automático da climatização, mantendo a temperatura desejada.

## Requisitos

- Microcontrolador ESP32
- Sensor de temperatura DS18B20
- Acesso a uma rede Wi-Fi
- Broker MQTT

## Instalação e Configuração

1. Certifique-se de ter todas as bibliotecas necessárias instaladas no seu ambiente de desenvolvimento.
2. Configure as informações de conexão Wi-Fi e MQTT no arquivo `config.py`.
3. Conecte o sensor de temperatura DS18B20 ao microcontrolador ESP32.
4. Certifique-se de que o microcontrolador esteja conectado aos dispositivos de controle de climatização (evaporadora, ciclos, etc.) conforme definido nos pinos GPIO configurados em `config.py`.

## Uso

1. Execute o script `main.py` no microcontrolador ESP32.
2. O dispositivo se conectará à rede Wi-Fi e ao broker MQTT especificados.
3. O sistema estará pronto para receber comandos MQTT para controle manual ou para operar automaticamente com base na temperatura atual e no setpoint definido.

## Funcionalidades

- **Controle Manual:** Você pode enviar comandos MQTT para controlar manualmente os dispositivos de climatização.
- **Modo Automático:** O sistema pode operar automaticamente com base na temperatura atual e no setpoint definido.
- **Monitoramento de Temperatura:** A temperatura ambiente é monitorada continuamente e publicada no broker MQTT para visualização remota.

## Tópicos MQTT

Os seguintes tópicos MQTT são utilizados para comunicação:

- `command/evaporadora`: Controla a evaporadora (ligado/desligado).
- `command/ciclo1`: Controla o ciclo 1 de refrigeração (ligado/desligado).
- `command/ciclo2`: Controla o ciclo 2 de refrigeração (ligado/desligado).
- `command/setpoint`: Define o setpoint de temperatura desejado.
- `command/automation`: Define o modo de operação (manual/automático).
- `state/evaporadora`: Estado atual da evaporadora (ligado/desligado).
- `state/ciclo1`: Estado atual do ciclo 1 (ligado/desligado).
- `state/ciclo2`: Estado atual do ciclo 2 (ligado/desligado).
- `temperatura`: Temperatura ambiente atual.

Certifique-se de configurar corretamente o broker MQTT para receber e processar esses tópicos.

## Contribuição

Contribuições são bem-vindas! Se você encontrar algum problema ou tiver sugestões para melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request no repositório do projeto.

## Autor

Este projeto foi desenvolvido por Mizael Lima.

---

Este documento fornece uma visão geral do projeto e orienta sobre sua instalação, configuração e uso. Certifique-se de consultar a documentação e os comentários no código-fonte para obter mais detalhes sobre a implementação.
