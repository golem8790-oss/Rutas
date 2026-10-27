#Contiene Greedy, Mochila 0/1 y la función que resume los resultados.
from itertools import combinations
def greedy(paquetes, peso_maximo, volumen_maximo):
    ordenados = sorted(
        paquetes,
        key=lambda p: p["prioridad"] / p["peso"],
        reverse=True
    )
    seleccionados = []
    peso_usado = 0
    volumen_usado = 0
    for paquete in ordenados:
        if (
            peso_usado + paquete["peso"] <= peso_maximo
            and volumen_usado + paquete["volumen"] <= volumen_maximo
        ):
            seleccionados.append(paquete)
            peso_usado += paquete["peso"]
            volumen_usado += paquete["volumen"]
    return seleccionados
def mochila_01(paquetes, peso_maximo, volumen_maximo):
    mejor_combinacion = []
    mejor_prioridad = 0
    for cantidad in range(1, len(paquetes) + 1):
        for combinacion in combinations(paquetes, cantidad):
            peso_total = sum(p["peso"] for p in combinacion)
            volumen_total = sum(p["volumen"] for p in combinacion)
            prioridad_total = sum(p["prioridad"] for p in combinacion)
            if (
                peso_total <= peso_maximo
                and volumen_total <= volumen_maximo
                and prioridad_total > mejor_prioridad
            ):
                mejor_prioridad = prioridad_total
                mejor_combinacion = list(combinacion)
    return mejor_combinacion
def calcular_resumen(seleccionados):
    return {
        "paquetes": seleccionados,
        "cantidad": len(seleccionados),
        "peso": sum(p["peso"] for p in seleccionados),
        "volumen": sum(p["volumen"] for p in seleccionados),
        "prioridad": sum(p["prioridad"] for p in seleccionados)
    }
