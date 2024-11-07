from ultralytics import YOLO
from threading import Thread
import psutil
import time

model = YOLO('yolov8n.pt')


arquivo = open('speed3.text' , 'a')
for i in range(300):
    source = 'images/img'+str(i+1)+'.jpg'
    # print(source)
    results = model(source, conf=0.5)  # list of Results objects
    # print(results[0].speed['postprocess'] + results[0].speed['preprocess'] + results[0].speed['inference'])
    soma = results[0].speed['postprocess'] + results[0].speed['preprocess'] + results[0].speed['inference']
    aux_inserir = str(soma)+ "\n"
    arquivo.write(aux_inserir)

arquivo.close()
