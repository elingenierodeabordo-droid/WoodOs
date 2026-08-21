import random

# Rodillo con emojis
rodillo = ["7️⃣", "🍒", "🍋", "🍊", "🍇", "🍉", "🔔", "⭐", "💎", "BAR", ]

# Tabla de pagos (multiplicadores)
pagos = {
    ("7️⃣", "7️⃣", "7️⃣"): 100,     # 100 * 50 = 5000
    ("BAR", "BAR", "BAR"): 20,
    ("💎", "💎", "💎"): 15,
    ("🔔", "🔔", "🔔"): 10,
    ("🍒", "🍒", "🍒"): 5,
    ("🍋", "🍋", "🍋"): 1,
    ("🍊", "🍊", "🍊"): 1,
    ("🍇", "🍇", "🍇"): 1,
    ("🍉", "🍉", "🍉"): 1,
}

APUESTA = 100  # apuesta fija

def tirar_rodillos():
    return (
        random.choice(rodillo),
        random.choice(rodillo),
        random.choice(rodillo)
    )

def calcular_pago(resultado):
    if resultado in pagos:
        return pagos[resultado] * APUESTA
    return 0

def jugar():
    dinero = 10000  # dinero inicial
    print("🎰 Bienvenido a la máquina 777 con EMOJIS 🎰")
    print(f"💰 Dinero inicial: {dinero}€")
    print(f"💵 Apuesta fija por tirada: {APUESTA}€\n")

    while dinero >= APUESTA:
        input("Pulsa ENTER para tirar...")
        dinero -= APUESTA

        resultado = tirar_rodillos()
        print("Rodillos:", " | ".join(resultado))

        ganancia = calcular_pago(resultado)
        if ganancia > 0:
            dinero += ganancia
            print(f"🎉 ¡Ganaste {ganancia}€! 🎉")
        else:
            print("❌ No ganaste esta vez.")

        print(f"💰 Dinero actual: {dinero}€\n")

        if dinero < APUESTA:
            print("😢 No tienes suficiente dinero para seguir jugando.")
            break

        seguir = input("¿Quieres seguir jugando? (s/n): ").lower()
        if seguir == "n":
            break

    print("Gracias por jugar. ¡Vuelve pronto! 😄")

jugar()
