# smart-chair

O projeto consiste em um gerenciador de atividade e medidores de conforto embutidos dentro de uma cadeira

Sensores utilizados
  Sensor de temperatura
  Sensor de presença
  Sensor de humidade
  Sensor de luminosidade
  
A integração é feita pela porta serial de um raspberry pi e um MBED onde segregaremos as responsabilidades de gerenciar os sensores e as informações para o usuário, o raspberry pi vai ser responsável por receber as informações e exibir de forma mais agradável para o usuário, enquanto o MBED vai gerar um json a partir dos retornos dos sensores por ele gerenciados

Lista de materiais:
  Sensor de temperatura
  Sensor de presença
  Sensor de humidade
  Sensor de luminosidade
  Raspberry PI
  Cabo para comunicação Serial
  MBED
