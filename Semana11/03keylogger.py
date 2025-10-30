# # pip install pynput

# from pynput import keyboard

# def on_press(key):
#     try:
#         with open("keys.txt", "a") as f:
#             f.write(str(key.char))
#     except AttributeError:
#         with open("keys.txt", "a") as f:
#             f.write("[" + str(key) + "]")

# listener = keyboard.Listener(on_press=on_press)
# listener.start()
# listener.join()

# import os
# import time
# import datetime
# import pyautogui

# OUT_DIR = "screenshots"
# os.makedirs(OUT_DIR, exist_ok=True)

# INTERVAL_SECONDS = 5  # cambiar según necesidad

# print("Capturando pantalla cada", INTERVAL_SECONDS, "segundos. Ctrl+C para detener.")
# try:
#     while True:
#         ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#         filename = os.path.join(OUT_DIR, f"screenshot_{ts}.png")
#         img = pyautogui.screenshot()
#         img.save(filename)
#         print("Guardado:", filename)
#         time.sleep(INTERVAL_SECONDS)
# except KeyboardInterrupt:
#     print("Detenido por usuario.")
import platform
import psutil
import json
import datetime

info = {}
info['timestamp'] = datetime.datetime.now().isoformat()
info['platform'] = {
    'system': platform.system(),
    'node': platform.node(),
    'release': platform.release(),
    'version': platform.version(),
    'machine': platform.machine(),
    'processor': platform.processor()
}
info['cpu'] = {
    'physical_cores': psutil.cpu_count(logical=False),
    'total_cores': psutil.cpu_count(logical=True),
    'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
    'cpu_percent': psutil.cpu_percent(interval=1)
}
svmem = psutil.virtual_memory()
info['memory'] = {
    'total': svmem.total,
    'available': svmem.available,
    'used': svmem.used,
    'percent': svmem.percent
}
info['disk'] = []
for p in psutil.disk_partitions():
    try:
        usage = psutil.disk_usage(p.mountpoint)
        info['disk'].append({
            'device': p.device, 'mountpoint': p.mountpoint, 'fstype': p.fstype,
            'total': usage.total, 'used': usage.used, 'free': usage.free, 'percent': usage.percent
        })
    except PermissionError:
        pass

with open("system_info.json", "w") as f:
    json.dump(info, f, indent=2)

print("Información del sistema guardada en system_info.json")
