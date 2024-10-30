import torch
from ultralytics import YOLO

# Verifica se o CUDA está disponível
if torch.cuda.is_available():
    device = 'cuda'
    print("GPU detectada e disponível para uso.")
else:
    device = 'cpu'
    print("GPU não detectada; usando CPU.")

model = YOLO('yolov8n.pt').to(device)
