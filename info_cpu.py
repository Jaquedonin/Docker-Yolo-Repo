import psutil
import time

men = psutil.virtual_memory()
print("MEMORIA", men)
processes = psutil.process_iter()
pid= 0
for process in processes:
    # print(f"PID: {process.pid}, Nome: {process.name()}")
    if (process.name() == "python3" ):
        pid = process.pid
# obter informações de uso da CPU
for i in range (6):
    process = psutil.Process(pid)  # PID 1 é o processo init no Linux
    # print(f"Nome: {process.threads()}, Status: {process.status()}")
    cpu_percent = process.cpu_percent()
    print(f"Uso da CPU: {cpu_percent}%")
    cpu_num = process.cpu_times()
    print(f"Número da CPU: {cpu_num}")
    memory = process.memory_percent()
    print(f"Uso de memória: {memory}")
    time.sleep(1)
