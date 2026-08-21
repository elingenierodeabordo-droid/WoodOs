import urllib.request

print(
    urllib.request.urlopen(
        "https://wttr.in/Zaragoza?format=3"
    ).read().decode()
)
