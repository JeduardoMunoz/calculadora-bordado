# ============================================================
# BASE DE DATOS — HISTORIAL DE COTIZACIONES
# Autor: Jesus Eduardo Munoz
# GitHub: JeduardoMunoz
# Version: 1.0 | Mayo 2026
# ============================================================

import sqlite3
from datetime import datetime

# Nombre del archivo de base de datos
# SQLite guarda todo en un solo archivo .db

DB_NOMBRE = "cotizaciones.db"

def crear_tabla ():
    # Conectamos al archivo de base de datos
    # Si no existe, SQLite lo crea automaticamente
    conexion = sqlite3.connect(DB_NOMBRE)

    # El cursor es el objeto que ejecuta comandos SQL
    cursor = conexion.cursor()

    # Creamos la tabla si no existe todavia
    # IF NOT EXISTS evita error si ya fue creada antes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cotizaciones (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha       TEXT    NOT NULL,
            puntadas    INTEGER NOT NULL,
            tarifa      REAL    NOT NULL,
            complejidad TEXT    NOT NULL,
            prenda      TEXT    NOT NULL,
            plataforma  TEXT    NOT NULL,
            modo        TEXT    NOT NULL,
            precio_final REAL   NOT NULL
        )
    """)

    # Guardamos los cambio
    conexion.commit()

    # Cerramos la conexion
    conexion.close()

def guardar_cotizacion(puntadas, tarifa, complejidad, prenda, plataforma, modo, precio_final):
    conexion = sqlite3.connect(DB_NOMBRE)
    cursor = conexion.cursor()

    # Obtenemos la fecha y hora actual
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insertamos una fila nueva en la tabla
    cursor.execute("""
        INSERT INTO cotizaciones
        (fecha, puntadas, tarifa, complejidad, prenda, plataforma, modo, precio_final)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (fecha, puntadas, tarifa, complejidad, prenda, plataforma, modo, precio_final))

    conexion.commit()
    conexion.close()

    print(f"  [Cotizacion guardada en historial]")


def obtener_historial(limite=20):
    # REFACTOR v1.1 — función extraída de ver_historial()
    # Motivo: ver_historial() mezclaba dos responsabilidades:
    #   1. obtener datos de la base de datos
    #   2. imprimir en consola
    # Al separar la consulta SQL en su propia función,
    # servidor.py puede obtener los datos sin duplicar el SQL.
    # Principio aplicado: DRY (Don't Repeat Yourself)
    conexion = sqlite3.connect(DB_NOMBRE)
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, fecha, puntadas, complejidad, prenda, modo, precio_final
        FROM cotizaciones
        ORDER BY fecha DESC
        LIMIT ?
    """, (limite,))
    filas = cursor.fetchall()
    conexion.close()
    return filas  # devuelve datos, no imprime


def ver_historial():
    # REFACTOR v1.1 — ahora delega la consulta a obtener_historial()
    # Antes: tenía su propia conexión y consulta SQL
    # Ahora: solo se encarga de imprimir — un solo trabajo
    filas = obtener_historial()

    if not filas:
        print("\nNo hay cotizaciones guardadas todavia.")
        return

    print("\n" + "=" * 60)
    print("   HISTORIAL DE COTIZACIONES")
    print("=" * 60)
    print(f"  {'#':<4} {'Fecha':<20} {'Puntadas':<10} {'Modo':<12} {'Precio'}")
    print("-" * 60)

    for fila in filas:
        id, fecha, puntadas, complejidad, prenda, modo, precio = fila
        print(f"  {id:<4} {fecha:<20} {puntadas:<10,} {modo:<12} ${precio:.2f}")

    print("=" * 60)


# --- PRUEBA ---
# Esto solo corre cuando ejecutas base_datos.py directamente
# No cuando lo importas desde otro archivo
if __name__ == "__main__":
    crear_tabla()
    print("Base de datos lista.")
    ver_historial()


