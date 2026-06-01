# ============================================================
# CALCULADORA DE PRECIOS — DIGITALIZACIÓN DE BORDADOS
# Autor: Jesús Eduardo Muñoz
# GitHub: JeduardoMunoz
# Versión: 2.0 | Mayo 2026
# ============================================================

from base_datos import crear_tabla, guardar_cotizacion

# --- SECCIÓN 1: PLATAFORMAS DE PAGO ---
PLATAFORMAS = {
    "binance": {"porcentaje": 0.001, "fijo": 0.00},
    "paypal":  {"porcentaje": 0.044, "fijo": 0.30},
    "zinli":   {"porcentaje": 0.030, "fijo": 0.00},
}

# --- SECCIÓN 2: COMPLEJIDAD DEL DISEÑO ---
COMPLEJIDAD = {
    "simple":   0.00,
    "medio":    0.20,
    "complejo": 0.40,
}

# --- SECCIÓN 3: DIFICULTAD DE LA TELA ---
# VALORES PENDIENTES DE VALIDACIÓN CON MERCADO REAL
PRENDAS = {
    "tela_plana": 0.00,
    "manga":      1.50,
    "gorra":      2.50,
}

# --- SECCIÓN 4: MODO DE PRECIO ---
# Define en qué etapa de negocio estás con ese cliente
# captacion: primeros clientes, necesitas reseñas, precio bajo
# estandar: precio real de tu trabajo
# premium: urgencia, cliente VIP, trabajo complejo extra

MODO_PRECIO = {
    "captacion": 0.40,  # cobras el 40% del precio real
    "estandar" : 1.00,  # cobras el 100% del precio real
    "premium"  : 1.30,  # cobras el 130% del precio real
}

# --- SECCIÓN 5: VALIDACIÓN ---
def validar_inputs(puntadas, tarifa, complejidad, prenda, plataforma,modo):
    if puntadas <= 0:
        return "Error: las puntadas deben ser mayor a 0."
    if tarifa <= 0:
        return "Error: la tarifa debe ser mayor a 0."
    if complejidad not in COMPLEJIDAD:
        return f"Error: complejidad '{complejidad}' no válida. Usa: simple, medio, complejo."
    if prenda not in PRENDAS:
        return f"Error: prenda '{prenda}' no válida. Usa: tela_plana, manga, gorra."
    if plataforma not in PLATAFORMAS:
        return f"Error: plataforma '{plataforma}' no válida. Usa: binance, paypal, zinli."
    if modo not in MODO_PRECIO:
        return f"Error: modo '{modo}' no válido. usa: captacion, estandar, premium."
    return None


# --- SECCIÓN 5: CÁLCULO ---
def calcular_precio(puntadas, tarifa, complejidad, prenda, plataforma, modo):
    error = validar_inputs(puntadas, tarifa, complejidad, prenda, plataforma, modo)
    if error:
        return error

    precio_base       = (puntadas / 1000) * tarifa
    cargo_complejidad = precio_base * COMPLEJIDAD[complejidad]
    cargo_prenda      = PRENDAS[prenda]
    subtotal          = precio_base + cargo_complejidad + cargo_prenda

    # Aplicamos el multiplicador de modo ANTES de la comisión
    subtotal_modo = subtotal * MODO_PRECIO[modo]

    cargo_fijo   = PLATAFORMAS[plataforma]["fijo"]
    porcentaje   = PLATAFORMAS[plataforma]["porcentaje"]
    precio_final = (subtotal_modo + cargo_fijo) / (1 - porcentaje)

    return round(precio_final, 2)


# --- SECCIÓN 6: MOSTRAR RESULTADO ---
def mostrar_resultado(puntadas, tarifa, complejidad, prenda, plataforma, modo):
    precio = calcular_precio(puntadas, tarifa, complejidad, prenda, plataforma, modo)

    if isinstance(precio, str):
        print(f"\n{precio}")
        return

    precio_base       = (puntadas / 1000) * tarifa
    cargo_complejidad = precio_base * COMPLEJIDAD[complejidad]
    cargo_prenda      = PRENDAS[prenda]
    subtotal          = precio_base + cargo_complejidad + cargo_prenda
    subtotal_modo     = subtotal * MODO_PRECIO[modo]

    print("\n" + "=" * 48)
    print("   COTIZACIÓN — DIGITALIZACIÓN DE BORDADOS")
    print("=" * 48)
    print(f"  Puntadas:           {puntadas:,}")
    print(f"  Tarifa por millar:  ${tarifa:.2f}")
    print(f"  Complejidad:        {complejidad}")
    print(f"  Prenda:             {prenda}")
    print(f"  Modo de precio:     {modo}")
    print(f"  Plataforma de pago: {plataforma}")
    print("-" * 48)
    print(f"  Precio base:        ${precio_base:.2f}")
    print(f"  Cargo complejidad:  ${cargo_complejidad:.2f}")
    print(f"  Cargo prenda:       ${cargo_prenda:.2f}")
    print(f"  Subtotal:           ${subtotal:.2f}")
    print("-" * 48)
    print(f"  PRECIO A COBRAR:    ${precio:.2f} USD")
    print(f"  (Incluye comisión de {plataforma})")
    print("=" * 48)

# Guardamos la cotizacion en el historial
    guardar_cotizacion(puntadas, tarifa, complejidad, prenda, plataforma, modo, precio)


# Inicializamos la base de datos
crear_tabla()

# --- SECCIÓN 7: PRUEBAS ---

# Mismo diseño exacto, tres modos distintos
# Así vemos SOLO el impacto del modo de precio

print("\n--- COMPARACION DE MODOS ---")
mostrar_resultado(8000, 2.50, "medio", "tela_plana", "paypal", "captacion")
mostrar_resultado(8000, 2.50, "medio", "tela_plana", "paypal", "estandar")
mostrar_resultado(8000, 2.50, "medio", "tela_plana", "paypal", "premium")