import math

print("Calculadora WoodOS")
print("Ingrese una operación o escriba q para salir...")
print("Use sqrt(número) para raíz cuardada o sin(número), cos(número), etc.")
while True:

    cuenta = input(">>> ")

    if cuenta.lower() in ["salir", "exit", "q"]:
        break

    try:

        resultado = eval(
            cuenta,
            {"__builtins__": None},
            {
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "pi": math.pi,
                "e": math.e
            }
        )

        print("=", resultado)

    except Exception as e:

        print("Error:", e)
