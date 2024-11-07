# API de Inferência com YOLOv8 e Kafka

Esta API permite enviar imagens para inferência utilizando o modelo YOLOv8 de detecção de objetos, com Apache Kafka para escalabilidade e processamento assíncrono.

## Estrutura do Projeto

- **`app.py`**: API Flask para receber imagens e consultar resultados de inferência.
- **`inference_service.py`**: Serviço de inferência que processa imagens do Kafka e publica os resultados.
- **`config.py`**: Configuração para Kafka, tópicos e variáveis de ambiente.
- **`Dockerfile`**: Configuração do ambiente Docker para a API Flask.
- **`docker-compose.yml`**: Configuração do Docker Compose para Kafka, Zookeeper e a API Flask em contêineres.
- **`models/`**: Diretório que contém o arquivo do modelo YOLOv8 (`yolov8n.pt`).
- **`static/`**: Diretório de arquivos temporários, incluindo:
  - **`temp_images/`**: Imagens temporárias recebidas pela API.
  - **`results/`**: Resultados de inferência (opcional).
- **`requirements.txt`**: Lista de dependências do projeto.
- **`README.md`**: Documentação do projeto.

## Pré-requisitos

- **Docker** e **Docker Compose** devem estar instalados na máquina.
- O arquivo do modelo YOLO (`yolov8n.pt`) deve estar na pasta `models/`.

## Como Executar o Projeto

### Passo a Passo

#### 1. **Clonar o repositório**:

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DA_PASTA>
```
Instalar Dependências Localmente (opcional, apenas se não for usar Docker):

   ```bash
   pip install -r requirements.txt
```
    

#### Executar o Docker Compose:

```bash
docker-compose up --build
```


Este comando:

    Inicia o Zookeeper, Kafka e a API Flask.
    A API estará acessível em http://localhost:5000.

Encerrar o Docker Compose:

    Para parar todos os serviços, use:

```bash
     docker-compose down
```        
### Endpoints da API
## 1. POST /predict

Envia uma imagem para inferência.

    URL: /predict
    Método HTTP: POST
    Headers: Content-Type: multipart/form-data
    Body: Envie a imagem no campo image.

Exemplo de uso com curl:

```bash

    curl -X POST -F "image=@caminho/para/imagem.jpg" http://localhost:5000/predict
```
Resposta de sucesso:

```
json
{
  "inference_id": "1696602223.432",
  "message": "Inference request sent."
}
```
Descrição: Retorna um ID de inferência (inference_id) que pode ser usado para consultar o resultado posteriormente.
#### 2. GET /results/<inference_id>

Consulta o resultado de uma inferência enviada anteriormente.

    URL: /results/<inference_id>
    Método HTTP: GET

Exemplo de uso com curl:


    curl http://localhost:5000/results/1696602223.432

Resposta de sucesso (quando a inferência está concluída):

```json

{
  "inference_id": "1696602223.432",
  "detections": [
    {
      "box": [100, 150, 200, 250],
      "confidence": 0.95
    }
  ],
  "inference_time": 0.23
}
```
Descrição: Retorna o tempo de inferência e as detecções (bounding boxes e confiança) para a imagem processada. Se o resultado não estiver disponível, retorna uma mensagem informando que o resultado ainda não está pronto.
Estrutura de Arquivos e Pastas


```plaintext

project_root/
│
├── app.py                    # API principal Flask
├── inference_service.py      # Serviço de inferência
├── config.py                 # Configurações para Kafka
├── Dockerfile                # Dockerfile para a API Flask
├── docker-compose.yml        # Configuração Docker Compose
├── requirements.txt          # Dependências do projeto
├── models/                   # Diretório para o modelo YOLOv8
│   └── yolov8n.pt            # Arquivo do modelo YOLOv8
├── static/                   # Arquivos temporários
│   ├── temp_images/          # Imagens temporárias recebidas pela API
│   └── results/              # Resultados de inferência (opcional)
└── README.md                 # Documentação do projeto
```

Notas e Considerações

    Escalabilidade: A arquitetura com Kafka permite que vários serviços de inferência sejam executados em paralelo para maior desempenho.
    Monitoramento: Pode-se configurar o Kafka para monitorar o uso de recursos, logs e rastreamento de erros.
    Limpeza: As imagens temporárias são removidas após o processamento para liberar espaço.

Dependências

Para instalar as dependências localmente, use:

```bash
pip install -r requirements.txt
```
Conteúdo do requirements.txt:
```plaintext
Flask==2.2.3
kafka-python==2.0.2
opencv-python-headless==4.5.5.62
ultralytics==8.0.0
torch==1.13.1
```
