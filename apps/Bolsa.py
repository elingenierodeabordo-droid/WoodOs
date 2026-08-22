import json
import urllib.request

def consultar_accion(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d"
    # Yahoo requiere un User-Agent para no bloquear la petición
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            datos = json.loads(res.read().decode("utf-8"))
            meta = datos["chart"]["result"][0]["meta"]
            
            precio_actual = meta["regularMarketPrice"]
            precio_previo = meta["chartPreviousClose"]
            variacion = ((precio_actual - precio_previo) / precio_previo) * 100
            
            return precio_actual, variacion
    except Exception as e:
        return None, None

def accion(accion):
  VERDE = "\033[32m"
  ROJO = "\033[31m"
  RESET = "\033[0m"
  
  precio, variacion = consultar_accion(accion.upper())
  
  if precio is not None:
      color = VERDE if variacion >= 0 else ROJO
      signo = "+" if variacion >= 0 else ""
      print(f"{accion} ${precio:.2f} ({color}{signo}{variacion:.2f}%{RESET})")


print("=================================================================================================================")
print("                                            BOLSA                                                                ")
print("=================================================================================================================")

accion("AAPL")
accion("NVDA")
accion("SONY")
accion("TSLA")
accion("ITX.MC")
accion("^IBEX")
opc = input("Introduce una acción o pulsa 0 para salir o 1 para leer la exención de responsabilidad")
if opc == "0":
    exit()

elif opc == "1":
    print("================================================================================")
    print("                    DESCARGO DE RESPONSABILIDAD Y AVISO LEGAL")
    print("                                     WoodOS")
    print("================================================================================\n")
    
    print("1. PROPÓSITO EXCLUSIVAMENTE INFORMATIVO Y EDUCATIVO")
    print("La información, precios de cotización, índices, porcentajes de variación y")
    print("cualquier otro dato financiero o bursátil proporcionado por esta aplicación")
    print("(\"WoodOS\") se ofrecen de manera exclusivamente informativa, ilustrativa y")
    print("educativa. En ningún caso dicho contenido constituye una oferta, recomendación,")
    print("incitación, patrocinio o asesoramiento profesional de inversión, ni un análisis")
    print("financiero formal.\n")
    
    print("2. AUSENCIA DE ASESORAMIENTO FINANCIERO PROFESIONAL")
    print("Ningún elemento de esta herramienta debe interpretarse como asesoramiento legal,")
    print("fiscal, financiero, comercial o de inversión. Si requiere asesoramiento")
    print("especializado para la gestión de su capital, consulte siempre a un profesional")
    print("certificado, regulado e independiente antes de tomar cualquier decisión")
    print("operativa o comercial.\n")
    
    print("3. FUENTES DE DATOS, RETRASOS E INEXACTITUDES")
    print("Los datos bursátiles mostrados en esta aplicación se obtienen mediante peticiones")
    print("a interfaces de programación (API) de proveedores públicos o de terceros.")
    print("El desarrollador no garantiza la veracidad, exactitud, integridad, vigencia o")
    print("continuidad de dichos datos.")
    print("- Los precios pueden presentar retrasos significativos respecto al mercado en")
    print("  tiempo real.")
    print("- Pueden producirse interrupciones en el servicio, errores en la captura de")
    print("  datos o inconsistencias ajenas al control de este software.\n")
    
    print("4. ADVERTENCIA DE RIESGO DE MERCADO")
    print("La negociación y comercio de activos financieros (acciones, divisas, índices,")
    print("criptomonedas, derivados, etc.) entraña un alto nivel de riesgo e implica la")
    print("posibilidad real de perder la totalidad del capital invertido. Las rentabilidades")
    print("y rendimientos pasados de cualquier activo no garantizan en ningún caso")
    print("resultados ni ganancias futuras.\n")
    
    print("5. LIMITACIÓN DE RESPONSABILIDAD Y EXENCIÓN DE DAÑOS")
    print("Bajo ninguna circunstancia el creador, desarrolladores o colaboradores del")
    print("proyecto WoodOS serán responsables ante el usuario o terceros por pérdidas")
    print("financieras, decisiones de inversión erróneas, daños directos, indirectos,")
    print("incidentales, emergentes, punitivos o lucros cesantes derivados del uso,")
    print("imposibilidad de uso o confianza depositada en la información proporcionada por")
    print("esta aplicación.\n")
    
    print("6. GARANTÍA DEL SOFTWARE (\"TAL CUAL\")")
    print("Este programa se distribuye bajo el principio de \"TAL CUAL\" (\"AS IS\"), sin")
    print("garantías de ningún tipo, ya sean explícitas o implícitas, incluyendo, entre")
    print("otras, las garantías de comerciabilidad, idoneidad para un propósito particular")
    print("o no infracción. El usuario asume de forma íntegra el riesgo derivado de la")
    print("ejecución y uso de este software.\n")
    
    print("================================================================================")

else:
  accion(opc)






