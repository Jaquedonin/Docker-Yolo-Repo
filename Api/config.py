# config.py
KAFKA_BROKER_URL = 'localhost:9092'          # Endereço do servidor Kafka
INFERENCE_REQUEST_TOPIC = 'inference_requests'
INFERENCE_RESULT_TOPIC = 'inference_results'
GROUP_ID = 'flask_inference_consumer_group'  # ID do grupo de consumidores
