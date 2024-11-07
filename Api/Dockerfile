# Usar uma imagem base com Python
FROM python:3.7

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar o arquivo de requisitos e instalar as dependências
COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip uninstall kafka

# Instalar pacotes adicionais
RUN apt-get update && \
    apt-get install -y python3 && \
    pip install --no-cache-dir requests requests_oauthlib kafka-python confluent-kafka docker Flask && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copiar o restante do código da API para o diretório de trabalho
COPY . .

# Expor a porta onde o Flask vai rodar
EXPOSE 5000

# Comando para iniciar a API
CMD ["python", "app.py"]
