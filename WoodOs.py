import os
import platform
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime
from time import sleep
import webbrowser
#from emoji import *
# Ruta base del script para generar rutas absolutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ===================================== PYFIGLET =======================================
try:
    from pyfiglet import Figlet
except ModuleNotFoundError:
    input("Se necesitan librerías esenciales. Pulse enter para instalar. Tamaño aproximado: 1.8 - 2.0 MB")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyfiglet", "--break-system-packages"])
    try:
        from pyfiglet import Figlet
    except ModuleNotFoundError:
        print("Error al instalar pyfiglet. Reinicie la aplicación.")
        sys.exit()



# =================================== COMPROBACION AUDIO ====================================
audioplayer = ""
if shutil.which("pw-play"):
    audioplayer = "pw-play"
elif shutil.which("paplay"):
    audioplayer = "paplay"
elif shutil.which("aplay"):
    audioplayer = "aplay"


def guardar_devmode(valor):
    ruta = os.path.join(BASE_DIR, ".devmode.dat")
    with open(ruta, "w") as f:
        f.write("1" if valor else "0")


def cargar_devmode():
    try:
        ruta = os.path.join(BASE_DIR, ".devmode.dat")
        with open(ruta, "r") as f:
            return f.read() == "1"
    except FileNotFoundError:
        return False


def guardar_passmode(valor):
    ruta = os.path.join(BASE_DIR, ".passmode.dat")
    with open(ruta, "w") as f:
        f.write(str(valor))


def cargar_passmode():
    try:
        ruta = os.path.join(BASE_DIR, ".passmode.dat")
        with open(ruta, "r") as f:
            return int(f.read())
    except Exception:
        return 3

def cargar_hotspot():
    return cargar_punto_acceso()

def cargar_punto_acceso():
    ruta = os.path.join(BASE_DIR, ".puntoacceso.txt")
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            lineas = [linea.strip() for linea in f if linea.strip()]
            if len(lineas) >= 2:
                return lineas[0], lineas[1]
    except Exception:
        pass

    return "WoodOS_AP", "12345678"
        
def estado_hotspot():
    nombre_ap, a = cargar_hotspot()
    res = subprocess.run(
        ["nmcli", "connection", "show", "--active"],
        capture_output=True, text=True
    )
    return nombre_ap in res.stdout

        
def guardar_punto_acceso(ssid, password):

    ruta = os.path.join(
        BASE_DIR,
        ".puntoacceso.txt"
    )

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(ssid + "\n")
        f.write(password)

def encender_hotspot(interfaz=None):
    ssid, password = cargar_punto_acceso()
    if not interfaz:
        interfaz = obtener_interfaz_wifi()

    # Validación crucial: si sigue siendo None, salimos
    if not interfaz:
        print("No se ha detectado ninguna interfaz Wi-Fi.")
        return False

    cmd = [
        "nmcli", "device", "wifi", "hotspot",
        "ifname", interfaz, "ssid", ssid, "password", password
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode == 0
        
def apagar_hotspot():
    nombre_ap, a = cargar_punto_acceso()
    res = subprocess.run(
        ["nmcli", "connection", "down", nombre_ap],
        capture_output=True, text=True
    )
    return res.returncode == 0

def ejecutar_sudo(comando):
    ruta_pass = os.path.join(BASE_DIR, ".woodos_pass")
    if ajustpass == 1 and os.path.exists(ruta_pass):
        with open(ruta_pass, "r") as f:
            password = f.read()
        return subprocess.run(
            ["sudo", "-S"] + comando,
            input=password + "\n",
            text=True
        )
    else:
        return subprocess.run(["sudo"] + comando)


def sonido(nombre):
    ruta = os.path.join(BASE_DIR, "sounds", nombre)
    if os.path.exists(ruta) and audioplayer:
        subprocess.Popen([audioplayer, ruta])


def guardar_ciudad(ciudad):
    ruta = os.path.join(BASE_DIR, ".ciudad.dat")
    with open(ruta, "w") as f:
        f.write(ciudad)


def cargar_ciudad():
    try:
        ruta = os.path.join(BASE_DIR, ".ciudad.dat")
        with open(ruta, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

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
def obtener_interfaz_wifi():
    resultado = subprocess.run(
        ["nmcli", "-t", "-f", "DEVICE,TYPE", "device", "status"],
        capture_output=True,
        text=True
    )

    for linea in resultado.stdout.splitlines():
        partes = linea.split(":")

        if len(partes) >= 2:
            dispositivo = partes[0]
            tipo = partes[1]

            if tipo == "wifi":
                return dispositivo

    return None

# ============================== GESTIÓN DE RED Y CONECTIVIDAD ==============================
def gestion_redes():
    while True:
        os.system("clear")
        print(titulo.renderText("Conectividad"))
        print("--- \uf1eb Wi-Fi ---")
        print("1. Escanear y conectarse a una red Wi-Fi")
        if devmode:
            print("2. Estado del adaptador y conexiones activas")
        print("3. Activar / Desactivar Wi-Fi")
        print("4. Activar / Desactivar Punto de Acceso (Hotspot)")
        print("\n--- \uf293 Bluetooth ---")
        print("5. Escanear dispositivos Bluetooth")
        print("6. Ver dispositivos emparejados")
        print("7. Conectar dispositivo Bluetooth")
        print("8. Activar / Desactivar Bluetooth")
        print()
        print("0. Volver")
        print()

        opc = input("Seleccione una opción: ").strip()

        if opc == "0":
            sonido("selection.wav")
            break

        # --- OPCIONES WI-FI ---
        elif opc == "1":
            sonido("selection.wav")
            os.system("clear")
            print(titulo.renderText("WiFi"))
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

                    input("\nPresione Enter para continuar...")

        elif opc == "2" and devmode:
            sonido("selection.wav")
            print("\n--- Estado de Dispositivos ---")
            subprocess.run(["nmcli", "device", "status"])
            print("\n--- Conexiones Activas ---")
            subprocess.run(["nmcli", "connection", "show", "--active"])
            input("\nPresione Enter para continuar...")

        elif opc == "3":
            sonido("selection.wav")
            estado = input("¿Activar o desactivar WiFi? (on/off): ").strip().lower()
            if estado in ["on", "off"]:
                subprocess.run(["nmcli", "radio", "wifi", estado])
                print(f"\nWiFi configurado en: {estado.upper()}")
            else:
                print("\nOpción no válida.")
            input("\nPresione Enter para continuar...")

        elif opc == "4":
            sonido("selection.wav")
            if not estado_hotspot():
                if encender_hotspot():
                    print("\nPunto de acceso activado.")
                else:
                    print("\nNo se pudo activar el punto de acceso.")
            else:
                if apagar_hotspot():
                    print("\nPunto de acceso desactivado.")
                else:
                    print("\nNo se pudo desactivar el punto de acceso.")
            input("\nPresione Enter para continuar...")

        # --- OPCIONES BLUETOOTH ---
        elif opc == "5":
            sonido("selection.wav")
            os.system("clear")
            print(titulo.renderText("Bluetooth"))
            print("\nBuscando dispositivos durante 5 segundos...\n")
            subprocess.run(["bluetoothctl", "power", "on"], capture_output=True)
            try:
                subprocess.run(["bluetoothctl", "--timeout", "5", "scan", "on"], capture_output=True, text=True)
                resultado = subprocess.run(["bluetoothctl", "devices"], capture_output=True, text=True)
                lineas = resultado.stdout.strip().splitlines()
                if lineas:
                    for l in lineas:
                        print(f" 🔵 {l}")
                else:
                    print("No se encontraron dispositivos cercanos.")
            except Exception as e:
                print("Error al escanear:", e)
            input("\nPresione Enter para continuar...")

        elif opc == "6":
            sonido("selection.wav")
            os.system("clear")
            print(titulo.renderText("Bluetooth"))
            print("\nDispositivos emparejados:\n")
            resultado = subprocess.run(["bluetoothctl", "paired-devices"], capture_output=True, text=True)
            if resultado.stdout.strip():
                print(resultado.stdout)
            else:
                print("No hay dispositivos emparejados.")
            input("\nPresione Enter para continuar...")

        elif opc == "7":
            sonido("selection.wav")
            mac = input("\nIntroduce la dirección MAC del dispositivo (ej. 00:11:22:33:44:55): ").strip()
            if mac:
                subprocess.run(["bluetoothctl", "pair", mac])
                res = subprocess.run(["bluetoothctl", "connect", mac], capture_output=True, text=True)
                if res.returncode == 0:
                    print("\nConexión establecida con éxito.")
                else:
                    print("\nError al conectar.")
            input("\nPresione Enter para continuar...")

        elif opc == "8":
            sonido("selection.wav")
            estado = input("¿Activar o desactivar Bluetooth? (on/off): ").strip().lower()
            if estado in ["on", "off"]:
                subprocess.run(["bluetoothctl", "power", estado])
                print(f"\nBluetooth configurado en: {estado.upper()}")
            else:
                print("\nOpción no válida.")
            input("\nPresione Enter para continuar...")
#======================================COLORES ANSI======================================================
MARRON = "\033[38;5;130m"
RST = "\033[0m"
TACH = "\033[9m"
ROJO = "\033[31m"
# ===================================== SETUP ======================================================
sistema = platform.system()
devmode = cargar_devmode()
ver = "1.4.4 beta"
ajustpass = cargar_passmode()
novedades = "Prueba el nuevo sistema de red y bluetooth! 🌐"
os.system("clear")


titulo = Figlet(font="soft")
reloj = Figlet(font="small")

paquetes = {
    "obs": "obs-studio",
    "vscode": "code",
    "visual studio code": "code",
    "chrome": "google-chrome-stable",
    "telegram": "telegram-desktop"
}

USUARIO_GITHUB = "elingenierodeabordo-droid"
REPO = "WoodOS"
RAMA = "main"
URL_VERSION = f"https://raw.githubusercontent.com/{USUARIO_GITHUB}/{REPO}/{RAMA}/version.txt"
URL_CODIGO = f"https://raw.githubusercontent.com/{USUARIO_GITHUB}/{REPO}/{RAMA}/woodos.py"
# ======================================== METEO ========================================================
def meteo(ciudad):
    if not ciudad:
        return "Ciudad no configurada"
    try:
        # Añadimos timeout de 3 segundos
        return urllib.request.urlopen(f"https://wttr.in/{ciudad}?format=3", timeout=3).read().decode()
    except Exception:
        return "Sin conexión"


# ==================================== GESTIÓN DE USUARIOS ===============================================
def cargar_usuario():
    ruta_usuario = os.path.join(BASE_DIR, ".usuario.dat")
    if os.path.exists(ruta_usuario):
        with open(ruta_usuario, "r") as f:
            return f.read().strip()

    usuario = input("Nombre de usuario: ")
    with open(ruta_usuario, "w") as f:
        f.write(usuario)
    return usuario


usuario = cargar_usuario()

USER_DIR = os.path.join(BASE_DIR, "Users", usuario)

os.makedirs(USER_DIR, exist_ok=True)
os.makedirs(os.path.join(USER_DIR, "Documentos"), exist_ok=True)
os.makedirs(os.path.join(USER_DIR, "Descargas"), exist_ok=True)
os.makedirs(os.path.join(USER_DIR, "Escritorio"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "apps"), exist_ok=True)

#=======================================GITHUB======================================================
def comprobar(version_actual):
    print("\n🔍 Buscando actualizaciones en GitHub...")
        try:
            req = urllib.request.urlopen(URL_VERSION, timeout=5)
            version_remota = req.read().decode("utf-8").strip()
    
            if version_remota != version_actual:
                print(f"\n🎉 ¡Nueva versión disponible! (Actual: {version_actual} | Nueva: {version_remota})")
                opc = input("¿Deseas instalarla ahora? (s/N): ").strip().lower()
                if opc == "s":
                    ruta_script = os.path.abspath(__file__)
                    print("⬇️ Descargando archivo principal...")
                    urllib.request.urlretrieve(URL_CODIGO, ruta_script)
                    
                    print("⬇️ Descargando aplicaciones...")
                    actualizar_apps()
                    
                    print("\n✅ ¡WoodOS y sus apps se han actualizado con éxito! Reiniciando...")
                    os.execv(sys.executable, [sys.executable] + sys.argv)
            else:
                print("✅ Estás en la versión más reciente.")
                
        except Exception as e:
            print(f"❌ Error al comprobar actualizaciones: {e}")



# ========================== BUCLE PRINCIPAL ============================================================
sleep(0.1)
sonido("startup.wav")

meteo_hoy = meteo(cargar_ciudad())
if cargar_ciudad() is None:
    ci = input("Introduce tu ciudad con la primera letra mayúscula: ")
    guardar_ciudad(ci)



while True:
    os.system("clear")
    # =============================== CONFIGURACIÓN DEL SISTEMA DE APPS ===============================
    apps = []
    ruta_apps = os.path.join(BASE_DIR, "apps")

    if os.path.exists(ruta_apps):
        for archivo in os.listdir(ruta_apps):
            if archivo.endswith(".py"):
                apps.append(archivo)

    # =============================== MENÚ PRINCIPAL ===============================
    print(MARRON, titulo.renderText("WoodOS"), RST)
    print(reloj.renderText(datetime.now().strftime("%H:%M")))
    print(novedades)
    print(meteo(cargar_ciudad()))
    print()

    if devmode:
        print("🛠 DEV MODE ACTIVADO")
        print()

    print("1. ⚙  Configuración")
    print("2. 📦 Apps")
    print("3. 🔌 Energía")
    if meteo_hoy != "Ciudad no configurada" and meteo_hoy != "Sin conexión":
        print("4. 🌡️ Ver pronósitico completo")
    print()
    print("0. Salir")

    menu = input("Seleccione opción o introduzca nombre del programa: ")

    # =============================== OPCIONES DEL MENÚ ===============================
    if menu == "0":
        sonido("selection.wav")
        print("Saliendo...")
        break

    elif menu == "1":
        sonido("selection.wav")
        os.system("clear")
        print("0. Volver")
        print("1. Activar/desactivar modo desarrollador")
        print("2. Información de WoodOS")
        print("3. Leer los Términos de uso")
        print("4. Ajustes de guardado de contraseña")
        print("5. Cambiar ciudad")
        print("6. Wifi y red")
        print("7. Buscar actualizaciones")
        config = input("Seleccione una opción: ")
        if config == "0":
            sonido("selection.wav")
        elif config == "1":
            sonido("selection.wav")
            input("Pulse Enter para activar/desactivar el modo desarrollador")
            devmode = not devmode
            guardar_devmode(devmode)
            print(f"El modo desarrollador está ahora {'activado' if devmode else 'desactivado'}")
            sleep(2)

        elif config == "2":
            sonido("selection.wav")
            print(f"WoodOS {ver} en {sistema} versión {platform.release()}")
            sleep(2)

        elif config == "3":
            sonido("selection.wav")
            terminos = input("¿Quieres leer los términos de uso? (s/N): ")
            if terminos.lower() == "s":
                try:
                    ruta_terminos = os.path.join(BASE_DIR, "terminos.txt")
                    with open(ruta_terminos, "r") as f:
                        print("\n" + f.read())
                    input("Pulsa enter para volver al menú")
                except FileNotFoundError:
                    print("No se ha encontrado el archivo terminos.txt.")
                    sleep(2)

        elif config == "4":
            sonido("selection.wav")
            print("\n🔐 Gestión de contraseña de administrador\n")
            print("1. Guardar la contraseña en este equipo")
            print("2. Pedir la contraseña al iniciar WoodOS")
            print("3. Pedir la contraseña cada vez que sea necesaria")
            sel = input("Seleccione una opción: ")

            ruta_pass = os.path.join(BASE_DIR, ".woodos_pass")

            if sel == "1":
                sonido("selection.wav")
                confirmar = input("¿Deseas continuar? (s/N): ")
                if confirmar.lower() == "s":
                    import getpass
                    password = getpass.getpass("🔑 Introduce tu contraseña: ")
                    resultado = subprocess.run(
                        ["sudo", "-S", "-v"],
                        input=password + "\n",
                        text=True,
                        capture_output=True
                    )
                    if resultado.returncode == 0:
                        with open(ruta_pass, "w") as f:
                            f.write(password)
                        ajustpass = 1
                        guardar_passmode(ajustpass)
                        print("Contraseña guardada correctamente.")
                        sleep(2)

            elif sel in ["2", "3"]:
                sonido("selection.wav")
                ajustpass = int(sel)
                guardar_passmode(ajustpass)
                if os.path.exists(ruta_pass):
                    os.remove(ruta_pass)
                sleep(2)

        elif config == "5":
            sonido("selection.wav")
            guardar_ciudad(input("Ciudad: "))
            
        elif config == "6":
            sonido("selection.wav")
            gestion_redes()
        
        elif config == "7":
            sonido("selection.wav")
            comprobar(ver)
            input("Pulsa enter para volver al menú")
        
    elif menu == "2":
        sonido("selection.wav")
        while True:
            os.system("clear")
            print(titulo.renderText("Apps"))
            print()

            opciones_apps = {}
            opcion_num = 1

            for app in apps:
                nombre_app = app[:-3]
                print(f"{opcion_num}. 📦 {nombre_app}")
                opciones_apps[str(opcion_num)] = app
                opcion_num += 1

            print("\ni. Instalar aplicación")
            print("u. Actualizar sistema")
            print("0. Volver\n")

            sel = input("> ")

            if sel == "0":
                sonido("selection.wav")
                break

            elif sel == "i":
                sonido("selection.wav")
                programa = input("Nombre del programa a instalar: ").lower()
                paquete = paquetes.get(programa, programa)
                print(f"Paquete seleccionado: {paquete}")
                resultado = ejecutar_sudo(["apt", "install", "-y", paquete])
                if resultado.returncode == 0:
                    print("Instalado mediante APT.")
                else:
                    print("APT ha fallado.")
                input("\nPulse Enter...")

            elif sel == "u":
                sonido("selection.wav")
                ejecutar_sudo(["apt", "update"])
                ejecutar_sudo(["apt", "full-upgrade", "-y"])
                if devmode:
                    ejecutar_sudo(["apt", "autoremove", "-y"])
                input("\nPulse Enter...")

            elif sel in opciones_apps:
                sonido("selection.wav")
                script = opciones_apps[sel]
                ruta_script = os.path.join(ruta_apps, script)
                print(f"\nEjecutando {script}...\n")
                try:
                    subprocess.run([sys.executable, ruta_script])
                except Exception as e:
                    print("\nError al ejecutar la aplicación:", e)
                input("\nPresione Enter para volver...")

            else:
                print("Opción no válida.")
                sleep(1)

    elif menu == "3":
        sonido("selection.wav")
        print("Opciones de apagado: ")
        print("0. Volver")
        print("1. Apagar")
        print("2. Suspender")
        print("3. Reiniciar")
        sel = input("Seleccione una opción: ")

        if sel == "0":
            sonido("selection.wav")
            sleep(0.01)
        elif sel == "1":
            sonido("shutdown.wav")
            ejecutar_sudo(["shutdown", "now"])
        elif sel == "2":
            sonido("shutdown.wav")
            ejecutar_sudo(["systemctl", "suspend"])
        elif sel == "3":
            sonido("shutdown.wav")
            ejecutar_sudo(["reboot"])
        else:
            print("Opción no válida")
            sleep(1.5)


    elif menu == "4":
        try:
            subprocess.run(["curl", f"wttr.in/{cargar_ciudad()}?lang=es"])
            
            input("Pulse enter para volver al menú...")
        except:
            print("Error.")

    
    
    else:
        try:
            subprocess.run(menu.split())
        except Exception:
            print("Error al ejecutar el comando")
            sleep(1.5)
