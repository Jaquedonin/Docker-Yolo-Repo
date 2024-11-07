import os

KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL', 'kafka:9092')
INFERENCE_REQUEST_TOPIC = os.getenv('INFERENCE_REQUEST_TOPIC', 'inference_request')
INFERENCE_RESULT_TOPIC = os.getenv('INFERENCE_RESULT_TOPIC', 'inference_result')
GROUP_ID = os.getenv('GROUP_ID', 'inference_group')
