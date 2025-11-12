from multiprocessing import Process
import os, time

def tarea(nombre):
    print(f"{nombre} ejecutándose en PID {os.getpid()}")
    time.sleep(1)

if __name__ == "__main__":
    p1 = Process(target=tarea, args=("Proceso 1",))
    p2 = Process(target=tarea, args=("Proceso 2",))
    p1.start(); p2.start()
    p1.join(); p2.join()
    print("Procesos terminados")
