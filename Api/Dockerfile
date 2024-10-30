# Usar uma imagem base com Python
FROM python:3.9-slim

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar o arquivo de requisitos e instalar as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da API para o diretório de trabalho
COPY . .

# Expor a porta onde o Flask vai rodar
EXPOSE 5000

# Comando para iniciar a API
CMD ["python", "app.py"]
