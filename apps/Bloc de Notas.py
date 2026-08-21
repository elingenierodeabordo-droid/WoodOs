import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(BASE_DIR)

config_file = os.path.join(BASE_DIR, ".usuario.dat")

usuario = "default"
if os.path.exists(config_file):
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            if contenido:
                usuario = os.path.basename(contenido)
    except IOError:
        print("Advertencia: No se pudo leer el archivo de configuración.")

USER_DIR = os.path.join(BASE_DIR, "Users", usuario)

try:
    os.makedirs(USER_DIR, exist_ok=True)
except PermissionError:
    print(f"Error crítico: No hay permisos para crear el directorio {USER_DIR}")
    exit(1)


def obtener_archivos_txt():
    txts = []
    for ruta, carpetas, archivos in os.walk(USER_DIR):
        for archivo in archivos:
            if archivo.endswith(".txt"):
                txts.append(os.path.join(ruta, archivo))
    return txts


def mostrar_lista():
    txts = obtener_archivos_txt()
    if not txts:
        print("\nNo se encontraron archivos .txt.")
    else:
        print("\nArchivos disponibles:")
        for idx, ruta in enumerate(txts, 1):
            ruta_relativa = os.path.relpath(ruta, USER_DIR)
            print(f"{idx}. {ruta_relativa}")
    return txts


def editar_archivo(ruta_archivo):
    lineas = []
    if os.path.exists(ruta_archivo):
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                lineas = [linea.rstrip("\r\n") for linea in f.readlines()]
        except IOError:
            print("Error al leer el archivo existente.")
            return

    while True:
        print("\n--- Contenido actual ---")
        if not lineas:
            print("(Archivo vacío)")
        else:
            for idx, linea in enumerate(lineas, 1):
                print(f"{idx}: {linea}")

        print("\nOpciones de edición:")
        print("1. Modificar una línea existente")
        print("2. Agregar nueva línea al final")
        print("3. Eliminar una línea")
        print("0. Guardar y salir")

        sub_opcion = input("Seleccione una opción: ").strip()

        if sub_opcion == "1":
            if not lineas:
                print("No hay líneas para modificar.")
                continue
            try:
                num = int(input("Número de línea a modificar: ")) - 1
                if 0 <= num < len(lineas):
                    nuevo_texto = input(f"Nuevo texto para la línea {num + 1}: ")
                    lineas[num] = nuevo_texto
                else:
                    print("Número fuera de rango.")
            except ValueError:
                print("Por favor, ingrese un número válido.")

        elif sub_opcion == "2":
            nueva_linea = input("Escriba el texto de la nueva línea: ")
            lineas.append(nueva_linea)

        elif sub_opcion == "3":
            if not lineas:
                print("No hay líneas para eliminar.")
                continue
            try:
                num = int(input("Número de línea a eliminar: ")) - 1
                if 0 <= num < len(lineas):
                    lineas.pop(num)
                    print("Línea eliminada.")
                else:
                    print("Número fuera de rango.")
            except ValueError:
                print("Por favor, ingrese un número válido.")

        elif sub_opcion == "0":
            try:
                with open(ruta_archivo, "w", encoding="utf-8") as f:
                    for linea in lineas:
                        f.write(linea + "\n")
                print("Cambios guardados exitosamente.")
            except IOError:
                print("Error: Ocurrió un problema al guardar el archivo.")
            break

        else:
            print("Opción no válida. Intente de nuevo.")


while True:
    print("\n--- Bloc de Notas ---")
    print("1. Leer archivo")
    print("2. Crear / Editar archivo")
    print("3. Borrar archivo")
    print("0. Salir")

    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1":
        archivos = mostrar_lista()
        if archivos:
            try:
                num = int(input("\nSeleccione el número del archivo a leer: ")) - 1
                if 0 <= num < len(archivos):
                    try:
                        with open(archivos[num], "r", encoding="utf-8") as f:
                            print(f"\n--- Contenido de {os.path.basename(archivos[num])} ---")
                            print(f.read())
                    except (FileNotFoundError, PermissionError):
                        print("Error: No se pudo leer el archivo (quizás fue eliminado o no tienes permisos).")
                else:
                    print("Número fuera de rango.")
            except ValueError:
                print("Por favor, ingrese un número válido.")

    elif opcion == "2":
        nombre_raw = input("\nEscriba el nombre del archivo (ej. nota.txt): ").strip()

        if not nombre_raw:
            print("Error: El nombre del archivo no puede estar vacío.")
            continue

        nombre = os.path.basename(nombre_raw)

        if not nombre.endswith(".txt"):
            nombre += ".txt"

        ruta_archivo = os.path.join(USER_DIR, nombre)
        editar_archivo(ruta_archivo)

    elif opcion == "3":
        archivos = mostrar_lista()
        if archivos:
            try:
                num = int(input("\nSeleccione el número del archivo a borrar: ")) - 1
                if 0 <= num < len(archivos):
                    confirmacion = input(f"¿Seguro que desea borrar '{os.path.basename(archivos[num])}'? (s/n): ").strip().lower()
                    if confirmacion == 's':
                        try:
                            os.remove(archivos[num])
                            print("Archivo eliminado exitosamente.")
                        except (FileNotFoundError, PermissionError):
                            print("Error: No se pudo eliminar el archivo. Es posible que ya no exista o esté en uso.")
                    else:
                        print("Operación cancelada.")
                else:
                    print("Número fuera de rango.")
            except ValueError:
                print("Por favor, ingrese un número válido.")

    elif opcion == "0":
        print("Saliendo del Bloc de Notas...")
        break

    else:
        print("Opción no válida. Intente de nuevo.")
