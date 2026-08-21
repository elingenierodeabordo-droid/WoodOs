import random
import time

# ==========================
# CONFIGURACIÓN
# =========================

DINERO_INICIAL = 1000
APUESTA_MINIMA = 10

PALOS = ["♠", "♥", "♦", "♣"]
VALORES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


# =========================
# CREAR BARAJA
# =========================

def crear_baraja():
    baraja = []

    for palo in PALOS:
        for valor in VALORES:
            baraja.append((valor, palo))

    random.shuffle(baraja)
    return baraja


# =========================
# VALOR DE LAS CARTAS
# =========================

def valor_carta(carta):
    valor = carta[0]

    if valor in ["J", "Q", "K"]:
        return 10

    if valor == "A":
        return 11

    return int(valor)


def calcular_puntuacion(mano):
    puntuacion = sum(valor_carta(carta) for carta in mano)

    ases = sum(1 for carta in mano if carta[0] == "A")

    while puntuacion > 21 and ases:
        puntuacion -= 10
        ases -= 1

    return puntuacion


# =========================
# MOSTRAR CARTAS
# =========================

def carta_texto(carta):
    return carta[0] + carta[1]


def mostrar_mano(nombre, mano, ocultar_primera=False):

    print(f"\n{nombre}")

    if ocultar_primera:
        cartas = ["🂠"] + [carta_texto(c) for c in mano[1:]]
        print(" | ".join(cartas))
    else:
        cartas = [carta_texto(c) for c in mano]
        print(" | ".join(cartas))

        puntuacion = calcular_puntuacion(mano)
        print(f"Valor: {puntuacion}")


# =========================
# ANIMACIÓN
# =========================

def animacion_reparto():
    print("\n🃏 Repartiendo", end="")

    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)

    print()


# =========================
# JUGAR UNA MANO
# =========================

def jugar_mano(dinero, estadisticas):

    # Comprobar apuesta
    while True:

        try:
            apuesta = int(input(f"\n💰 ¿Cuánto quieres apostar? (mínimo {APUESTA_MINIMA}€): "))

            if apuesta < APUESTA_MINIMA:
                print("❌ La apuesta es demasiado baja.")
                continue

            if apuesta > dinero:
                print("❌ No tienes suficiente dinero.")
                continue

            break

        except ValueError:
            print("❌ Introduce un número.")

    dinero -= apuesta

    baraja = crear_baraja()

    jugador = []
    crupier = []

    # Repartir
    jugador.append(baraja.pop())
    crupier.append(baraja.pop())
    jugador.append(baraja.pop())
    crupier.append(baraja.pop())

    animacion_reparto()

    print("\n" + "=" * 40)
    print("🃏 NUEVA MANO")
    print("=" * 40)

    mostrar_mano("🤖 CRUPIER", crupier, ocultar_primera=True)
    mostrar_mano("👤 TÚ", jugador)

    # =========================
    # BLACKJACK DEL JUGADOR
    # =========================

    if calcular_puntuacion(jugador) == 21:

        print("\n🎉 ¡BLACKJACK!")

        # Blackjack paga 3:2
        ganancia = int(apuesta * 1.5)
        dinero += apuesta + ganancia

        print(f"💰 Has ganado {ganancia}€")
        print(f"💵 Saldo: {dinero}€")

        estadisticas["manos"] += 1
        estadisticas["victorias"] += 1
        estadisticas["blackjacks"] += 1

        return dinero

    # =========================
    # TURNO DEL JUGADOR
    # =========================

    while True:

        puntuacion = calcular_puntuacion(jugador)

        if puntuacion > 21:
            print("\n💥 ¡TE HAS PASADO!")
            print(f"💸 Pierdes {apuesta}€")

            estadisticas["manos"] += 1
            estadisticas["derrotas"] += 1

            return dinero

        print("\n" + "-" * 40)
        print("¿Qué quieres hacer?")
        print("1️⃣ Pedir carta")
        print("2️⃣ Plantarse")
        print("3️⃣ Doblar")

        opcion = input("👉 ")

        # PEDIR
        if opcion == "1":

            carta = baraja.pop()
            jugador.append(carta)

            print(f"\n🃏 Has recibido: {carta_texto(carta)}")

            mostrar_mano("👤 TÚ", jugador)

        # PLANTARSE
        elif opcion == "2":

            print("\n✋ Te plantas.")
            break

        # DOBLAR
        elif opcion == "3":

            if len(jugador) != 2:
                print("❌ Solo puedes doblar con tus dos primeras cartas.")
                continue

            if dinero < apuesta:
                print("❌ No tienes suficiente dinero para doblar.")
                continue

            dinero -= apuesta
            apuesta *= 2

            print(f"\n💰 Apuesta doblada: {apuesta}€")

            carta = baraja.pop()
            jugador.append(carta)

            print(f"🃏 Has recibido: {carta_texto(carta)}")

            mostrar_mano("👤 TÚ", jugador)

            if calcular_puntuacion(jugador) > 21:
                print("\n💥 ¡TE HAS PASADO!")

                estadisticas["manos"] += 1
                estadisticas["derrotas"] += 1

                return dinero

            break

        else:
            print("❌ Opción no válida.")

    # =========================
    # TURNO DEL CRUPIER
    # =========================

    print("\n" + "=" * 40)
    print("🤖 TURNO DEL CRUPIER")
    print("=" * 40)

    mostrar_mano("🤖 CRUPIER", crupier)

    while calcular_puntuacion(crupier) < 17:

        time.sleep(0.7)

        carta = baraja.pop()
        crupier.append(carta)

        print(f"\n🃏 El crupier roba: {carta_texto(carta)}")

        mostrar_mano("🤖 CRUPIER", crupier)

    puntuacion_jugador = calcular_puntuacion(jugador)
    puntuacion_crupier = calcular_puntuacion(crupier)

    print("\n" + "=" * 40)
    print("🏁 RESULTADO")
    print("=" * 40)

    mostrar_mano("🤖 CRUPIER", crupier)
    mostrar_mano("👤 TÚ", jugador)

    # =========================
    # RESULTADO
    # =========================

    if puntuacion_crupier > 21:

        print("\n💥 ¡EL CRUPIER SE PASA!")
        ganancia = apuesta
        dinero += apuesta * 2

        print(f"🎉 ¡Ganas {ganancia}€!")

        estadisticas["victorias"] += 1

    elif puntuacion_jugador > puntuacion_crupier:

        print("\n🎉 ¡HAS GANADO!")

        ganancia = apuesta
        dinero += apuesta * 2

        print(f"💰 +{ganancia}€")

        estadisticas["victorias"] += 1

    elif puntuacion_jugador < puntuacion_crupier:

        print("\n❌ HAS PERDIDO")
        estadisticas["derrotas"] += 1

    else:

        print("\n🤝 EMPATE")
        dinero += apuesta

        estadisticas["empates"] += 1

    estadisticas["manos"] += 1

    print(f"\n💵 Saldo: {dinero}€")

    return dinero


# =========================
# ESTADÍSTICAS
# =========================

def mostrar_estadisticas(dinero, estadisticas):

    print("\n")
    print("╔══════════════════════════════╗")
    print("║       📊 ESTADÍSTICAS        ║")
    print("╠══════════════════════════════╣")
    print(f"║ 💰 Saldo:       {dinero:>10}€ ║")
    print(f"║ 🃏 Manos:       {estadisticas['manos']:>10}   ║")
    print(f"║ 🏆 Victorias:   {estadisticas['victorias']:>10}   ║")
    print(f"║ ❌ Derrotas:    {estadisticas['derrotas']:>10}   ║")
    print(f"║ 🤝 Empates:     {estadisticas['empates']:>10}   ║")
    print(f"║ 🃏 Blackjacks:  {estadisticas['blackjacks']:>10}   ║")
    print("╚══════════════════════════════╝")


# =========================
# JUEGO PRINCIPAL
# =========================

def blackjack():

    dinero = DINERO_INICIAL

    estadisticas = {
        "manos": 0,
        "victorias": 0,
        "derrotas": 0,
        "empates": 0,
        "blackjacks": 0
    }

    print("""
╔════════════════════════════════════╗
║                                    ║
║          🃏 BLACKJACK 🃏           ║
║                                    ║
║       ¡21 es el objetivo!          ║
║                                    ║
╚════════════════════════════════════╝
""")

    print(f"💰 Dinero inicial: {dinero}€")
    print(f"💵 Apuesta mínima: {APUESTA_MINIMA}€")

    while dinero >= APUESTA_MINIMA:

        print("\n" + "=" * 40)
        print(f"💰 SALDO: {dinero}€")
        print("=" * 40)

        print("\n1️⃣ Jugar")
        print("2️⃣ Estadísticas")
        print("3️⃣ Salir")

        opcion = input("\n👉 Elige una opción: ")

        if opcion == "1":

            dinero = jugar_mano(dinero, estadisticas)

        elif opcion == "2":

            mostrar_estadisticas(dinero, estadisticas)

        elif opcion == "3":

            break

        else:

            print("❌ Opción no válida.")

    if dinero < APUESTA_MINIMA:

        print("\n💸 Te has quedado sin dinero.")

    mostrar_estadisticas(dinero, estadisticas)

    print("\n👋 Gracias por jugar al Blackjack.")


# =========================
# INICIAR
# =========================

blackjack()