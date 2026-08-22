import shutil

total, used, free = shutil.disk_usage("/")
libre_gb = free / (1024**3)
total_gb = total / (1024**3)
porcentaje_usado = (used / total) * 100
