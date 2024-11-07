from kafka import KafkaProducer, KafkaConsumer
from ultralytics import YOLO
import json
import config
import os
import torch

# Configuração do dispositivo para a inferência
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Configuração do Kafka Consumer
consumer = KafkaConsumer(
    config.INFERENCE_REQUEST_TOPIC,
    bootstrap_servers=config.KAFKA_BROKER_URL,
    group_id='inference_service_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

# Configuração do Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=config.KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Carregar o modelo YOLO para o dispositivo disponível
model = YOLO('models/yolov8n.pt').to(device)

def process_inference_request():
    """Processa cada solicitação de inferência recebida via Kafka."""
    for message in consumer:
        data = message.value
        inference_id = data.get('inference_id')
        image_path = data.get('image_path')

        # Verifica se a mensagem possui os dados necessários
        if not inference_id or not image_path:
            print("Erro: 'inference_id' ou 'image_path' ausente na mensagem.")
            continue

        # Realiza a inferência
        try:
            # Realiza a inferência no YOLO com a imagem recebida
            results = model(image_path)
            detections = []

            # Processa os resultados, extraindo os bounding boxes e confiabilidade
            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                    confidence = float(box.conf[0].cpu().numpy())
                    detections.append({"box": [x1, y1, x2, y2], "confidence": confidence})

            # Monta o resultado com o tempo de inferência, se disponível
            result_data = {
                'inference_id': inference_id,
                'detections': detections,
                'inference_time': results[0].speed['inference'] if hasattr(results[0], 'speed') else None
            }

            # Envia o resultado da inferência para o Kafka
            producer.send(config.INFERENCE_RESULT_TOPIC, value=result_data)
            producer.flush()  # Garante que a mensagem seja enviada imediatamente

        except Exception as e:
            print(f"Erro ao processar {inference_id}: {str(e)}")

        # Remove a imagem temporária após o processamento
        if os.path.exists(image_path):
            os.remove(image_path)
        else:
            print(f"O caminho da imagem {image_path} não existe.")

if __name__ == '__main__':
    process_inference_request()
