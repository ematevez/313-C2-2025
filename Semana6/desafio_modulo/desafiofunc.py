import random

# Determinar ganador de la ronda
def verificar_ganador_ronda(jugador: int, maquina: int) -> str:
    """
    Devuelve "Jugador", "Máquina" o "Empate" según las elecciones.
    1 = Piedra, 2 = Papel, 3 = Tijera
    """
    if jugador == maquina:
        return "Empate"

    # Reglas de victoria
    if (jugador == 1 and maquina == 3) or \
        (jugador == 2 and maquina == 1) or \
        (jugador == 3 and maquina == 2):
        return "Jugador"
    else:
        return "Máquina"


# Verificar si la partida sigue
def verificar_estado_partida(aciertos_jugador: int, aciertos_maquina: int, ronda_actual: int) -> bool:
    """
    True si la partida continúa, False si finaliza.
    Finaliza si:
        - Alguien ganó 2 veces seguidas
        - O se jugaron 3 rondas
    """
    # Si ya se jugaron 3 rondas
    if ronda_actual >= 3:
        return False
    # Si alguien llegó a 2 aciertos consecutivos
    if aciertos_jugador >= 2 or aciertos_maquina >= 2:
        return False
    return True


# Ganador final de la partida
def verificar_ganador_partida(aciertos_jugador: int, aciertos_maquina: int) -> str:
    """
    Devuelve "Jugador" o "Máquina" según quién ganó más rondas.
    En caso de empate se manejará fuera (reglas de desempate).
    """
    if aciertos_jugador > aciertos_maquina:
        return "Jugador"
    else:
        return "Máquina"


#  Convertir elección numérica en texto
def mostrar_elemento(eleccion: int) -> str:
    elementos = {1: "Piedra", 2: "Papel", 3: "Tijera"}
    return elementos.get(eleccion, "Desconocido")


# Lógica completa del juego
def jugar_piedra_papel_tijera() -> str:
    """
    Ejecuta la partida completa al mejor de 3 rondas,
    con final anticipado si alguien gana 2 seguidas
    o con rondas extra si hay empate en 3 rondas.
    Devuelve "Jugador" o "Máquina" según el ganador final.
    """
    print("=== 🪨📄✂️ ¡Piedra, Papel o Tijera! ===\n")
    ronda = 0
    aciertos_jugador = 0
    aciertos_maquina = 0
    victorias_consecutivas_jugador = 0
    victorias_consecutivas_maquina = 0

    while True:
        ronda += 1
        print(f"\n--- Ronda {ronda} ---")

        # Entrada del jugador validada
        while True:
            try:
                jugador = int(input("Elige: 1=Piedra, 2=Papel, 3=Tijera: "))
                if jugador in (1, 2, 3):
                    break
                else:
                    print("❗ Opción inválida, elige 1, 2 o 3.")
            except ValueError:
                print("❗ Debes ingresar un número (1, 2 o 3).")

        maquina = random.randint(1, 3)

        print(f"Tú eliges: {mostrar_elemento(jugador)}")
        print(f"La máquina elige: {mostrar_elemento(maquina)}")

        resultado = verificar_ganador_ronda(jugador, maquina)
        if resultado == "Jugador":
            print("🏆 Ganas esta ronda!")
            aciertos_jugador += 1
            victorias_consecutivas_jugador += 1
            victorias_consecutivas_maquina = 0
        elif resultado == "Máquina":
            print("🤖 La máquina gana esta ronda.")
            aciertos_maquina += 1
            victorias_consecutivas_maquina += 1
            victorias_consecutivas_jugador = 0
        else:
            print("🤝 Empate en esta ronda.")
            victorias_consecutivas_jugador = 0
            victorias_consecutivas_maquina = 0

        print(f"Marcador -> Jugador: {aciertos_jugador} | Máquina: {aciertos_maquina}")

        # Verificar final por dos victorias consecutivas
        if victorias_consecutivas_jugador == 2 or victorias_consecutivas_maquina == 2:
            break

        # Verificar si se jugaron 3 rondas
        if ronda >= 3 and aciertos_jugador != aciertos_maquina:
            break

        # Si hay empate en 3 rondas, se continúa automáticamente
        if ronda >= 3 and aciertos_jugador == aciertos_maquina:
            print("Empate total, se juega una ronda extra!")

    ganador = verificar_ganador_partida(aciertos_jugador, aciertos_maquina)
    print(f"\n🎉 ¡Ganador de la partida: {ganador}!")
    return ganador


# Ejecución si se ejecuta directamente
if __name__ == "__main__":
    jugar_piedra_papel_tijera()
