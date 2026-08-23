import os

contraseñas_comunes = ["12345678",
                       "123456789",
                       "password",
                      	"1234567890",
                      	"skibidi,
                      	1234567,
                      	pakistan123
                        assword,


def escanear_redes():
    try:
        # Se elimina "--separator" porque nmcli no lo soporta
        resultado = subprocess.run(
            [
                "nmcli",
                "-t",
                "-f", "SSID,SIGNAL,SECURITY",
                "device", "wifi", "list"
            ],
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL
        )

        if resultado.returncode != 0:
            print("Error al escanear las redes.")
            if resultado.stderr:
                print(resultado.stderr.strip())
            return []

        redes = []
        ssids_vistos = set()

        for linea in resultado.stdout.splitlines():
            if not linea.strip():
                continue

            # Separamos por los 2 últimos puntos ':' para no romper nombres de red complejos
            partes = linea.rsplit(":", 2)

            if len(partes) == 3:
                ssid = partes[0].replace(r"\:", ":").strip()
                señal = partes[1].strip()
                seguridad = partes[2].strip()

                # Ignoramos redes sin nombre (ocultas) y repetidas
                if ssid and ssid not in ssids_vistos:
                    ssids_vistos.add(ssid)
                    redes.append((ssid, señal, seguridad))

        return redes

    except Exception as e:
        print("Error al escanear:", e)
        return []

def crack(ssid, password):
  while not exito:
    for i in contraseñas_comunes:
      




os.system("clear")
print("\nBuscando redes disponibles...\n")

# Reutilizamos la función que separa correctamente por "|"
redes = escanear_redes()

if not redes:
    print("No se encontraron redes disponibles.")
    input("\nPresione Enter para continuar...")
    continue

print("Redes disponibles:\n")
for i, (ssid, señal, seguridad) in enumerate(redes, 1):
    print(f"{i}. 📶 {ssid} | {señal}% | {seguridad}")

print("\n0. Volver")
sel = input("\nSelecciona el número de la red a la que conectar: ").strip()

if sel == "0":
    continue

if sel.isdigit():
    idx = int(sel) - 1
    if 0 <= idx < len(redes):
        ssid_elegido = redes[idx][0]
        seguridad = redes[idx][2]

        cmd = ["nmcli", "device", "wifi", "connect", ssid_elegido]

        # Si la red requiere contraseña (diferente de "--" o vacía)
        if seguridad and seguridad != "--":
            password = input(f"Contraseña para '{ssid_elegido}': ").strip()
            cmd.extend(["password", password])

        print(f"\nConectando a '{ssid_elegido}'...")
        res = subprocess.run(cmd, capture_output=True, text=True)

        if res.returncode == 0:
            print("¡Conectado con éxito!")
        else:
            print("Error al conectar:")
            print(res.stderr.strip() if res.stderr else res.stdout.strip())
