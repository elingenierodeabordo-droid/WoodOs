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
opc = input("Introduce una acción o pulsa 0 para salir")
if not opc == "0":
  accion(opc)
else:
  exit()






