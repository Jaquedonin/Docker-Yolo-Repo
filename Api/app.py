from flask import Flask, request, jsonify
from kafka import KafkaProducer, KafkaConsumer
import json
import config
import time
import os

app = Flask(__name__)

# Configuração do Kafka Producer e Consumer
producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

consumer = KafkaConsumer(
    config.INFERENCE_RESULT_TOPIC,
    bootstrap_servers=config.KAFKA_BROKER_URL,
    group_id=config.GROUP_ID,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

# Armazenamento temporário para resultados de inferência
inference_results = {}

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    # Recebe a imagem e gera um ID de inferência único
    image = request.files['image']
    inference_id = str(time.time())
    image_path = f'static/temp_images/temp_{inference_id}.jpg'
    image.save(image_path)

    # Publica a solicitação de inferência no Kafka
    data = {
        'inference_id': inference_id,
        'image_path': image_path
    }
    producer.send(config.INFERENCE_REQUEST_TOPIC, value=data)

    return jsonify({"inference_id": inference_id, "message": "Inference request sent."}), 202


@app.route('/results/<inference_id>', methods=['GET'])
def results(inference_id):
    # Verifica se há um resultado disponível para o ID de inferência
    if inference_id in inference_results:
        result = inference_results.pop(inference_id)
        return jsonify(result), 200
    else:
        return jsonify({"message": "Result not available yet. Try again later."}), 202


def listen_for_results():
    # Listener que recebe resultados de inferência do Kafka
    for message in consumer:
        result = message.value
        inference_id = result['inference_id']
        inference_results[inference_id] = result  # Armazena o resultado na memória


if __name__ == '__main__':
    from threading import Thread

    # Inicia o listener para resultados de inferência
    listener_thread = Thread(target=listen_for_results)
    listener_thread.start()

    app.run(host='0.0.0.0', port=5000)
