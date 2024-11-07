from flask import Flask, request, jsonify
from kafka import KafkaProducer, KafkaConsumer
import json
import config
import time
import os

app = Flask(__name__)

# Configuração do Kafka Producer para envio de solicitações de inferência
producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Caminho do arquivo para salvar os tempos de inferência
TIME_LOG_FILE = '/data/shared/inference_times.txt'  # Ajuste para volume compartilhado

@app.route('/batch_inference', methods=['POST'])
def batch_inference():
    if 'images' not in request.files:
        return jsonify({"error": "No images provided"}), 400

    images = request.files.getlist('images')
    inference_results = []

    # Envia cada imagem para o Kafka para processamento
    for image in images:
        inference_id = str(time.time())
        temp_dir = 'static/temp_images'
        
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        image_path = os.path.join(temp_dir, image.filename)
        image.save(image_path)

        data = {
            'inference_id': inference_id,
            'image_path': image_path
        }
        producer.send(config.INFERENCE_REQUEST_TOPIC, value=data)

        inference_results.append({
            "inference_id": inference_id,
            "message": "Inference request sent."
        })

    # Garantir que todas as mensagens foram enviadas
    producer.flush()

    return jsonify({"batch_results": inference_results}), 202


@app.route('/inference_log', methods=['GET'])
def get_inference_log():
    """Endpoint para ler os tempos de inferência salvos no arquivo."""
    if os.path.exists(TIME_LOG_FILE):
        with open(TIME_LOG_FILE, 'r') as file:
            times = file.readlines()
        return jsonify({"inference_times": times}), 200
    else:
        return jsonify({"error": "Inference log file not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
