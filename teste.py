from ultralytics import YOLO
from threading import Thread
import psutil
import time
import os
from PIL import Image, ImageDraw

# Inicializa variáveis de processo
processes = psutil.process_iter()  # Obtém a lista de processos em execução
pid = 0  # Inicializa o identificador do processo (PID) como 0
arquivo_process = open('process.text', 'a')  # Abre um arquivo de texto para registrar o uso de CPU e memória

# Define se as imagens com bounding boxes devem ser salvas
save_images_with_boxes = True  # Defina para False se não quiser salvar as imagens com caixas

# Cria a pasta "out" se ainda não existir
os.makedirs('out', exist_ok=True)  # Garante que a pasta "out" existe para salvar imagens com bounding boxes

# Obtém o PID do processo atual do Python
for process in processes:
    if process.name() == "python3":
        pid = process.pid  # Atribui o PID do processo Python atual

# Define a classe de thread para monitoramento de CPU e memória
class Th(Thread):
    def __init__(self, num):
        Thread.__init__(self)
        self.num = num
        self.running = True  # Variável para controlar a execução da thread

    def run(self):
        try:
            while self.running:
                process = psutil.Process(pid)
                cpu_percent = process.cpu_percent(interval=2)
                print(f"Uso da CPU: {cpu_percent}%")
                memory = process.memory_percent()
                print(f"Uso de memória: {memory}%")
                aux_escrita = f"Uso da CPU: {cpu_percent}%, Uso de memória: {memory}%\n"
                arquivo_process.write(aux_escrita)
                time.sleep(1)
        except KeyboardInterrupt:
            print("Monitoramento interrompido.")
        finally:
            arquivo_process.close()
            print("THREAD FINALIZADA!!!!!")

# Cria e inicia a thread de monitoramento
a = Th(1)
a.start()

try:
    # Carrega o modelo YOLOv8n com uso de GPU
    model = YOLO('yolov8n.pt').to('cuda')
    
    # Abre o arquivo para salvar os tempos de processamento
    arquivo = open('speed3.text', 'a')

    # Executa a inferência em um conjunto de imagens
    for i in range(300):
        source = f'images/img{i+1}.jpg'
        results = model(source, conf=0.5)  # Inferência no YOLO
        soma = results[0].speed['postprocess'] + results[0].speed['preprocess'] + results[0].speed['inference']
        aux_inserir = f"{soma}\n"
        arquivo.write(aux_inserir)
        
        # Exibe a saída do modelo
        print(f"\nResultados da imagem {source}:")
        for det in results[0].boxes:
            classe_idx = int(det.cls)  # Índice da classe detectada
            classe_nome = model.names[classe_idx]  # Nome da classe usando model.names
            confianca = float(det.conf)  # Converte confiança para float
            coords = det.xywh.tolist()  # Converte coordenadas para lista
            print(f"Classe: {classe_nome} (Índice: {classe_idx}), Confiança: {confianca:.2f}, Coordenadas: {coords}")

        # Desenhar e salvar a imagem com bounding boxes usando Pillow, se habilitado
        if save_images_with_boxes:
            # Carrega a imagem original
            img = Image.open(source)
            draw = ImageDraw.Draw(img)
            
            # Desenha cada bounding box
            for det in results[0].boxes:
                coords = det.xyxy.tolist()  # Coordenadas no formato [x1, y1, x2, y2]
                x1, y1, x2, y2 = map(int, coords[0])  # Converte para int para desenhar
                classe_nome = model.names[int(det.cls)]  # Nome da classe usando model.names
                confianca = float(det.conf)  # Converte para float
                draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
                draw.text((x1, y1), f"{classe_nome} {confianca:.2f}", fill="red")
            
            # Salva a imagem com bounding boxes na pasta "out"
            save_path = f'out/img{i+1}_boxed.jpg'
            img.save(save_path)
            print(f"Imagem com bounding boxes salva em: {save_path}")

except KeyboardInterrupt:
    print("Execução interrompida pelo usuário.")
finally:
    arquivo.close()
    a.running = False  # Para a thread de monitoramento
    a.join()           # Espera a thread terminar
