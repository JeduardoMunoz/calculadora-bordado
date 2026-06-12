# ============================================================
# SERVIDOR WEB — CALCULADORA DE BORDADOS
# Autor: Jesus Eduardo Munoz
# GitHub: JeduardoMunoz
# Version: 1.0 | Mayo 2026
# ============================================================

from flask import Flask, render_template, request, jsonify
from calculadora import calcular_precio, COMPLEJIDAD, PRENDAS, PLATAFORMAS, MODO_PRECIO
# REFACTOR v1.1 — agregado obtener_historial, eliminado ver_historial
# Motivo: la ruta /historial necesita datos, no impresión en consola
# Se eliminó también "import sqlite3" — ya no hay SQL directo en este archivo
from base_datos import crear_tabla, guardar_cotizacion, obtener_historial

app = Flask(__name__)

# Inicializamos la base de datos al arrancar
crear_tabla()


@app.route("/")
def index():
    # Cargamos las opciones para el formulario
    opciones = {
        "complejidad": list(COMPLEJIDAD.keys()),
        "prendas":     list(PRENDAS.keys()),
        "plataformas": list(PLATAFORMAS.keys()),
        "modos":       list(MODO_PRECIO.keys())
    }
    return render_template("index.html", opciones=opciones)


@app.route("/calcular", methods=["POST"])
def calcular():
    # Recibimos los datos del formulario
    datos = request.get_json()

    puntadas    = int(datos["puntadas"])
    tarifa      = float(datos["tarifa"])
    complejidad = datos["complejidad"]
    prenda      = datos["prenda"]
    plataforma  = datos["plataforma"]
    modo        = datos["modo"]

    # Calculamos el precio
    precio = calcular_precio(puntadas, tarifa, complejidad, prenda, plataforma, modo)

    # Si hay error de validacion lo devolvemos
    if isinstance(precio, str):
        return jsonify({"error": precio})

    # Calculamos el desglose para mostrar
    precio_base       = (puntadas / 1000) * tarifa
    cargo_complejidad = precio_base * COMPLEJIDAD[complejidad]
    cargo_prenda      = PRENDAS[prenda]
    subtotal          = precio_base + cargo_complejidad + cargo_prenda

    # Guardamos en base de datos
    guardar_cotizacion(puntadas, tarifa, complejidad, prenda, plataforma, modo, precio)

    return jsonify({
        "precio_base":       round(precio_base, 2),
        "cargo_complejidad": round(cargo_complejidad, 2),
        "cargo_prenda":      round(cargo_prenda, 2),
        "subtotal":          round(subtotal, 2),
        "precio_final":      precio,
        "plataforma":        plataforma,
        "modo":              modo
    })


@app.route("/historial")
def historial():
    # REFACTOR v1.1 — eliminada consulta SQL duplicada
    # Antes: este bloque tenía su propia conexión sqlite3 y cursor
    # Ahora: delega completamente a obtener_historial() en base_datos.py
    # Resultado: el SQL existe en un solo lugar del proyecto
    filas = obtener_historial(limite=20)
    cotizaciones = []
    for fila in filas:
        cotizaciones.append({
            "id":          fila[0],
            "fecha":       fila[1],
            "puntadas":    fila[2],
            "complejidad": fila[3],
            "prenda":      fila[4],
            "modo":        fila[5],
            "precio":      fila[6]
        })
    return jsonify(cotizaciones)


if __name__ == "__main__":
    app.run(debug=True)