#Recibe los formularios, registra paquetes y vehículos, llama a los algoritmos y entrega los resultados a la página web
from flask import Flask, render_template, request, redirect, url_for #Importa herramientas de Flask para crear la web y manejar formularios.
from algoritmos import greedy, mochila_01, calcular_resumen  #
from rutas import dijkstra, grafo
import csv

#crea la aplicación y guarda los datos
app = Flask(__name__)
paquetes = []
flota = [
    {
        "id": 1,
        "nombre": "Camioneta 1",
        "peso_maximo": 100,
        "volumen_maximo": 1.0
    }
]
#Funcion qye muuestra la pagina inicial
def mostrar_inicio(resultados=None):
    return render_template(
        "index.html",
        paquetes=paquetes,
        flota=flota,
        puntos=list(grafo.keys()), #obtiene los nombres de las ubicaciones del grafo y los envía a la página
        resultados=resultados
    )
@app.route("/")
def inicio():
    return mostrar_inicio()
@app.route("/registrar", methods=["POST"])
def registrar():
    peso = float(request.form["peso"])
    altura = float(request.form["altura"])
    ancho = float(request.form["ancho"])
    profundidad = float(request.form["profundidad"])
    prioridad = int(request.form["prioridad"])
    tipo = request.form["tipo"]
    ubicacion = request.form["ubicacion"]
    if (
        peso <= 0 or altura <= 0 or ancho <= 0 or profundidad <= 0
        or prioridad < 1 or prioridad > 10
    ):
        return "Datos incorrectos. Revisa peso, dimensiones y prioridad.", 400
    paquete = {
        "id": len(paquetes) + 1,
        "peso": peso,
        "altura": altura,
        "ancho": ancho,
        "profundidad": profundidad,
        "volumen": altura * ancho * profundidad / 1000000,
        "tipo": tipo,
        "prioridad": prioridad,
        "ubicacion": ubicacion
    }
    paquetes.append(paquete)
    return redirect(url_for("inicio"))
@app.route("/registrar_vehiculo", methods=["POST"])
def registrar_vehiculo():
    nombre = request.form["nombre"].strip()
    peso_maximo = float(request.form["peso_maximo"])
    volumen_maximo = float(request.form["volumen_maximo"])
    if not nombre or peso_maximo <= 0 or volumen_maximo <= 0:
        return "Datos incorrectos del vehículo.", 400
    flota.append({
        "id": len(flota) + 1,
        "nombre": nombre,
        "peso_maximo": peso_maximo,
        "volumen_maximo": volumen_maximo
    })
    return redirect(url_for("inicio"))
@app.route("/cargar_csv", methods=["POST"])
def cargar_csv():
    archivo = request.files["archivo"]
    if not archivo.filename.endswith(".csv"):
        return "Debes seleccionar un archivo CSV.", 400
    lector = csv.DictReader(
        archivo.stream.read().decode("utf-8-sig").splitlines()
    )
    for fila in lector:
        ubicacion = fila["ubicacion"].strip()
        if ubicacion not in grafo:
            return (
                "Ubicación no válida en el CSV: " + ubicacion
                + ". Usa una de las ubicaciones de la lista.",
                400
            )
        peso = float(fila["peso"])
        altura = float(fila["altura"])
        ancho = float(fila["ancho"])
        profundidad = float(fila["profundidad"])
        prioridad = int(fila["prioridad"])
        if (
            peso <= 0 or altura <= 0 or ancho <= 0 or profundidad <= 0
            or prioridad < 1 or prioridad > 10
        ):
            return "Hay datos incorrectos en el archivo CSV.", 400
        paquetes.append({
            "id": len(paquetes) + 1,
            "peso": peso,
            "altura": altura,
            "ancho": ancho,
            "profundidad": profundidad,
            "volumen": altura * ancho * profundidad / 1000000,
            "tipo": fila["tipo"].strip(),
            "prioridad": prioridad,
            "ubicacion": ubicacion
        })
    return redirect(url_for("inicio"))
@app.route("/optimizar", methods=["POST"])
def optimizar():
    metodo = request.form["metodo"]
    pendientes = paquetes.copy()
    resultados = []
    for vehiculo in flota:
        if metodo == "greedy":
            seleccionados = greedy(
                pendientes,
                vehiculo["peso_maximo"],
                vehiculo["volumen_maximo"]
            )
        else:
            seleccionados = mochila_01(
                pendientes,
                vehiculo["peso_maximo"],
                vehiculo["volumen_maximo"]
            )
        resumen = calcular_resumen(seleccionados)
        # Calcular el recorrido desde Centro por las ubicaciones asignadas
        recorrido = ["Centro"]
        distancia_total = 0
        ubicacion_actual = "Centro"
        for paquete in seleccionados:
            destino = paquete["ubicacion"]
            camino, distancia = dijkstra(ubicacion_actual, destino)
            if camino is not None:
                recorrido.extend(camino[1:])
                distancia_total += distancia
                ubicacion_actual = destino
        resumen["vehiculo"] = vehiculo["nombre"]
        resumen["recorrido"] = recorrido
        resumen["distancia"] = distancia_total
        resumen["peso_restante"] = (
            vehiculo["peso_maximo"] - resumen["peso"]
        )
        resumen["volumen_restante"] = (
            vehiculo["volumen_maximo"] - resumen["volumen"]
        )
        resultados.append(resumen)
        # Retirar los paquetes asignados para no duplicarlos
        for paquete in seleccionados:
            pendientes.remove(paquete)
    return mostrar_inicio({
        "metodo": metodo,
        "vehiculos": resultados,
        "sin_asignar": pendientes
    })
if __name__ == "__main__":
    app.run(debug=True)