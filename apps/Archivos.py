import os
import shutil


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

with open(os.path.join(BASE_DIR, ".usuario.dat"), "r") as f:
    usuario = f.read().strip()

USER_DIR = os.path.join(
    BASE_DIR,
    "Users",
    usuario
)

ruta_actual = USER_DIR
#=============================BUCLE==========================================
while True:
    os.system("clear")
    print("\n" + "=" * 60)
    print("Explorador de archivos")
    print("Ruta:", ruta_actual)
    print("=" * 60)

    elementos = sorted(
        [
            e for e in os.listdir(ruta_actual)
            if not e.startswith(".")
        ]
    )
    if elementos:
        for i, elemento in enumerate(elementos, start=1):

            ruta = os.path.join(ruta_actual, elemento)

            if os.path.isdir(ruta):
                print(f"{i}. 📁 {elemento}")
            else:
                print(f"{i}.{elemento}")

    else:
        #La carpeta está vacía
        print("Vacía.")
        
    print("\n0. Salir")
    print("s. Subir carpeta")
    print("n. Nueva carpeta")
    print("t. Nuevo archivo de texto")
    print("b. Borrar archivo")
    print("r. Renombrar")

    opcion = input("> ")

    if opcion == "0":
        break

    elif opcion == "s":

        nueva_ruta = os.path.dirname(ruta_actual)

        if nueva_ruta != ruta_actual:
            ruta_actual = nueva_ruta

    elif opcion == "b":
        indice = 0
        indice = int(input("Seleccione el archivo/carpeta a borrar: ")) - 1
        
        if 0 <= indice < len(elementos):

            nombre = elementos[indice]

            ruta_seleccionada = os.path.join(
                ruta_actual,
                nombre
            )

            if os.path.isfile(ruta_seleccionada):
                os.remove(ruta_seleccionada)

            elif os.path.isdir(ruta_seleccionada):
                shutil.rmtree(ruta_seleccionada)
            
    elif opcion == "n":

        nombre = input(
            "Nombre de la carpeta: "
        ).strip()

        if nombre:

            os.makedirs(
                os.path.join(
                    ruta_actual,
                    nombre
                ),
                exist_ok=True
            )    
            
    elif opcion == "r":

        indice = int(input("Seleccione el archivo/carpeta a renombrar: ")) - 1

        if 0 <= indice < len(elementos):

            nombre = elementos[indice]

            ruta_seleccionada = os.path.join(
                ruta_actual,
                nombre
            )

            nuevo = input(
                "Nuevo nombre: "
            )

            os.rename(
                ruta_seleccionada,
                os.path.join(ruta_actual, nuevo)
            )

    elif opcion == "t":

        nombre = input(
            "Nombre del archivo: "
        ).strip()

        if not nombre.endswith(".txt"):
            nombre += ".txt"

        ruta = os.path.join(
            ruta_actual,
            nombre
        )

        with open(
            ruta,
            "w",
            encoding="utf-8"
        ) as f:
            pass
            
            
            
    elif opcion.isdigit():

        indice = int(opcion) - 1

        if 0 <= indice < len(elementos):

            nombre = elementos[indice]

            ruta_seleccionada = os.path.join(
                ruta_actual,
                nombre
            )

            if os.path.isdir(ruta_seleccionada):

                ruta_actual = ruta_seleccionada

            else:

                print("\n" + "=" * 60)
                print(nombre)
                print("=" * 60)

                try:

                    with open(
                        ruta_seleccionada,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        print(f.read(3000))

                except Exception:

                    print(
                        "No se puede mostrar este archivo."
                    )

                input(
                    "\nPulse Enter para continuar..."
                )

    else:

        print("Opción no válida.")
