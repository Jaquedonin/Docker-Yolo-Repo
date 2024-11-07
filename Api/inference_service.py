import os
import json
import logging
from kafka import KafkaProducer, KafkaConsumer
from ultralytics import YOLO
import torch
import config

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Configuração de logging
logging.basicConfig(
    level=logging.DEBUG,  # Nível de log (DEBUG para mostrar tudo)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/data/shared/inference_service.log'),  # Arquivo de log
        logging.StreamHandler()  # Exibe também no terminal
    ]
)

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

model = YOLO('models/yolov8n.pt').to(device)

TIME_LOG_FILE = '/data/shared/inference_times.txt'  # Log gravado no diretório compartilhado

def process_inference_request():
    for message in consumer:
        data = message.value
        inference_id = data.get('inference_id')
        image_path = data.get('image_path')

        if not inference_id or not image_path:
            logging.error("Erro: 'inference_id' ou 'image_path' ausente na mensagem.")
            continue

        # Verifica se a imagem existe no caminho compartilhado
        shared_image_path = f'/data/shared/{image_path}'
        if not os.path.exists(shared_image_path):
            logging.error(f"Erro: A imagem {shared_image_path} não foi encontrada.")
            continue

        # Realiza a inferência
        try:
            logging.info(f"Processando requisição de inferência {inference_id} para a imagem {image_path}")
            results = model(shared_image_path)
            detections = []
            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                    confidence = float(box.conf[0].cpu().numpy())
                    detections.append({"box": [x1, y1, x2, y2], "confidence": confidence})

            total_inference_time = (
                results[0].speed['postprocess'] +
                results[0].speed['preprocess'] +
                results[0].speed['inference']
            )
            with open(TIME_LOG_FILE, 'a') as file:
                file.write(f"{total_inference_time}\n")

            result_data = {
                'inference_id': inference_id,
                'detections': detections,
                'inference_time': total_inference_time
            }

            producer.send(config.INFERENCE_RESULT_TOPIC, value=result_data)
            producer.flush()

            logging.info(f"Inferência {inference_id} processada com sucesso. Detections: {detections}")

        except Exception as e:
            logging.error(f"Erro ao processar {inference_id}: {str(e)}")

        # Remove a imagem temporária após o processamento
        if os.path.exists(shared_image_path):
            os.remove(shared_image_path)
            logging.info(f"Imagem {shared_image_path} removida após o processamento.")

if __name__ == '__main__':
    process_inference_request()
