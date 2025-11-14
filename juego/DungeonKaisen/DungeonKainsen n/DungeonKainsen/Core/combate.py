# core/combate.py
# Lógica de combate: D20 y cálculo simple de ataque.
import random  # random para lanzar el d20

def lanzar_d20():
    """Devuelve un entero 1..20."""
    return random.randint(1, 20)

def calcular_ataque(acd_enemigo, bonificador):
    """
    Lanza un d20 y compara con la ACD (Armor Class/Clase de Armadura) del enemigo.
    Retorna tupla: (resultado_dado:int, exito:bool, critico:bool, mensaje:str)
    Mensajes: "BLACK FLASH" para crítico, "Pega" para golpe normal, "fallo" o "ayy..." para fallos.
    """
    resultado_dado = lanzar_d20()
    total_golpe = resultado_dado + bonificador
    critico = resultado_dado == 20
    fallo_critico = resultado_dado == 1

    if total_golpe >= acd_enemigo:
        if critico:
            return resultado_dado, True, True, "BLACK FLASH"
        return resultado_dado, True, False, "Pega"
    elif fallo_critico:
        return resultado_dado, False, False, "ayy..."
    else:
        return resultado_dado, False, False, "fallo"