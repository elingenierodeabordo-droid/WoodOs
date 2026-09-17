primes = []

r = int(input("Introduzca iteraciones: "))

if r <= 0:
    r = 1

i = 2

for a in range(r):
    es_primo = True

    for p in primes:
        if p * p > i:
            break

        if i % p == 0:
            es_primo = False
            break

    if es_primo:
        primes.append(i)
        print(i, "ha resultado ser primo")

    i += 1
