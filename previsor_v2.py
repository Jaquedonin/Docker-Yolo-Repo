from ultralytics import YOLO
from threading import Thread
import psutil
import time

#process var
# processes = psutil.process_iter()
# pid= 0
# arquivo_process = open('process.text' , 'a')
# # Get process id
# for process in processes:
#     # print(f"PID: {process.pid}, Nome: {process.name()}")
#     if (process.name() == "python3" ):
#         pid = process.pid

# #define thread
# class Th(Thread):
#     def __init__ (self, num):
#         Thread.__init__(self)
#         self.num = num

#     def run(self):
#         for i in range (30):
#             process = psutil.Process(pid)  # PID 1 é o processo init no Linux
#             # print(f"Nome: {process.threads()}, Status: {process.status()}")
#             cpu_percent = process.cpu_percent(interval=2)
#             print(f"Uso da CPU: {cpu_percent}%")
#             cpu_num = process.cpu_times()
#             print(f"Número da CPU: {cpu_num}")
#             memory = process.memory_percent()
#             print(f"Uso de memória: {memory}%")
#             aux_escrita = "Uso da CPU: "+str(cpu_percent)+ " Uso de memória: "+str(memory)+"\n"
#             # velocidade.append(aux_inserir)
#             arquivo_process.write(aux_escrita)
#             time.sleep(1)

#         arquivo_process.close()
#         print("THREAD FINALIZADA!!!!!")
# #create and call a thread
# a = Th(1)
# a.start()

# Load a pretrained YOLOv8n model
model = YOLO('yolov8n.pt')

# Define path to the image file
# velocidade = []
arquivo = open('speed3.text' , 'a')
for i in range(300):
    source = 'images/img'+str(i+1)+'.jpg'
    # print(source)
    # Run inference on the source
    results = model(source, conf=0.5)  # list of Results objects
    # print(results[0].speed['postprocess'] + results[0].speed['preprocess'] + results[0].speed['inference'])
    soma = results[0].speed['postprocess'] + results[0].speed['preprocess'] + results[0].speed['inference']
    aux_inserir = str(soma)+ "\n"
    # velocidade.append(aux_inserir)
    arquivo.write(aux_inserir)

arquivo.close()
