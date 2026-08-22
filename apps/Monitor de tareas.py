import shutil
import subprocess
import os
import time

total, used, free = shutil.disk_usage("/")
libre_disco = free / (1024**3)
total_disco = total / (1024**3)
porcentaje_usado_disco = (used / total) * 100
ram_res = subprocess.run(["free", "-h"], capture_output=True, text=True)
try:
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp_cpu = int(f.read().strip()) / 1000.0  # Devuelve grados Celsius
except FileNotFoundError:
    temp_cpu = "Sin datos"

def obtener_uso_cpu():
    def leer_stat():
        with open("/proc/stat", "r") as f:
            linea = f.readline().split()
            # Suma de todos los tiempos de CPU
            valores = [float(x) for x in linea[1:]]
            idle = valores[3] + valores[4]  # idle + iowait
            total = sum(valores)
            return idle, total

    idle1, total1 = leer_stat()
    time.sleep(0.5)  # Espera medio segundo para calcular la diferencia
    idle2, total2 = leer_stat()

    total_diff = total2 - total1
    idle_diff = idle2 - idle1

    cpu_usada_pct = (1.0 - (idle_diff / total_diff)) * 100
    return round(cpu_usada_pct, 1)

print("=================================================================================")
print("                              MONITOR DE TAREAS                                  ")
print("=================================================================================")
print("CPU:")
print(f"Temperatura: {temp_cpu}")
print(f"Uso: {obtener_uso_cpu()}")
print()
print("RAM:")
print(f"{ram_res}")









