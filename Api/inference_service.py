from kafka import KafkaConsumer, KafkaProducer
from ultralytics import YOLO
import json
import config
import os
import time
import torch

# Configuração do Kafka
consumer = KafkaConsumer(
    config.INFERENCE_REQUEST_TOPIC,
    bootstrap_servers=config.KAFKA_BROKER_URL,
    group_id='inference_service_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Carrega o modelo YOLO
model = YOLO('models/yolov8n.pt').to('cuda' if torch.cuda.is_available() else 'cpu')

def process_inference_request():
    for message in consumer:
        data = message.value
        inference_id = data['inference_id']
        image_path = data['image_path']

        # Realiza a inferência
        try:
            results = model(image_path, conf=0.5)

            # Processa resultados e coleta coordenadas dos bounding boxes
            detections = []
            for box in results[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detections.append({"box": [x1, y1, x2, y2], "confidence": float(box.conf[0])})

            # Cria o resultado com o tempo de processamento
            result_data = {
                'inference_id': inference_id,
                'detections': detections,
                'inference_time': results[0].speed['inference']
            }

            # Publica o resultado no Kafka
            producer.send(config.INFERENCE_RESULT_TOPIC, value=result_data)

        except Exception as e:
            print(f"Error processing {inference_id}: {str(e)}")

        # Remove a imagem temporária após processamento
        os.remove(image_path)


if __name__ == '__main__':
    process_inference_request()
