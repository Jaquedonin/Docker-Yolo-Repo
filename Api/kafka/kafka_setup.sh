#!/bin/bash
# Executar após o Kafka estar rodando para criar os tópicos necessários

docker exec -it kafka /bin/bash <<EOF
kafka-topics.sh --create --topic inference_requests --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
kafka-topics.sh --create --topic inference_results --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
EOF
