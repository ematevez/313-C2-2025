# # Facturación del Servicio de Agua Potable
# # Entradas: solicita el consumo en m³ y el tipo de cliente.
# # Cálculos básicos: cargo fijo + (consumo × $200).
# # Reglas: aplica bonificaciones o recargos según el tipo de cliente y consumo.
# # Descuento especial residencial: si corresponde.
# # IVA: se aplica sobre el subtotal final.
# # Salida: muestra todo el desglose, con dos decimales y separadores de miles para mayor claridad.

# # --- Entrada de datos ---
# consumo = float(input("Ingrese la cantidad de m³ consumidos: "))
# tipo = input("Tipo de cliente (Residencial/Comercial/Industrial): ").strip().lower()

# # --- Datos fijos ---
# CARGO_FIJO = 7000
# COSTO_M3 = 200
# IVA = 0.21

# # --- Cálculo del costo por consumo ---
# costo_consumo = consumo * COSTO_M3
# subtotal = CARGO_FIJO + costo_consumo  # sin bonificaciones ni recargos

# bonificacion = 0
# recargo = 0

# # --- Reglas según tipo de cliente ---
# if tipo == "residencial":
#     if consumo < 30:
#         bonificacion += 0.10 * costo_consumo
#     elif consumo > 80:
#         recargo += 0.15 * costo_consumo

#     # Descuento especial si subtotal (sin impuestos ni bonificaciones) < 35000
#     if subtotal < 35000:
#         bonificacion += 0.05 * subtotal

# elif tipo == "comercial":
#     if consumo > 300:
#         bonificacion += 0.12 * costo_consumo
#     elif consumo > 150:
#         bonificacion += 0.08 * costo_consumo
#     if consumo < 50:
#         recargo += 0.05 * costo_consumo

# elif tipo == "industrial":
#     if consumo > 1000:
#         bonificacion += 0.30 * costo_consumo
#     elif consumo > 500:
#         bonificacion += 0.20 * costo_consumo
#     if consumo < 200:
#         recargo += 0.10 * costo_consumo
# else:
#     print("Tipo de cliente inválido. Debe ser Residencial, Comercial o Industrial.")
#     exit()

# # --- Subtotal con bonificaciones y recargos ---
# subtotal_ajustado = subtotal - bonificacion + recargo

# # --- IVA ---
# iva = subtotal_ajustado * IVA

# # --- Total final ---
# total = subtotal_ajustado + iva

# # --- Mostrar desglose ---
# print("\n--- DETALLE DE FACTURACIÓN ---")
# print(f"Consumo: {consumo} m³")
# print(f"Cargo fijo: ${CARGO_FIJO:,.2f}")
# print(f"Costo por consumo: ${costo_consumo:,.2f}")
# print(f"Subtotal (sin ajustes): ${subtotal:,.2f}")
# print(f"Bonificaciones: -${bonificacion:,.2f}")
# print(f"Recargos: +${recargo:,.2f}")
# print(f"Subtotal con ajustes: ${subtotal_ajustado:,.2f}")
# print(f"IVA (21%): +${iva:,.2f}")
# print(f"TOTAL A PAGAR: ${total:,.2f}")

# Tarifa base:
#Todas las facturas incluyen un cargo fijo de $7000 ademas del costo por consumo.

# # Sistema de Facturación de Agua Potable
# print("SISTEMA DE FACTURACIÓN DE AGUA POTABLE")
# print("======================================")

# # Solicitar datos al usuario
# try:
#     consumo = float(input("Ingrese la cantidad de metros cúbicos consumidos: "))
# except ValueError:
#     print("ERROR: Debe ingresar un número válido para el consumo.")
#     exit()

# print("\nTipos de cliente disponibles:")
# print("1. Residencial")
# print("2. Comercial") 
# print("3. Industrial")
# tipo_cliente = input("Ingrese el tipo de cliente: ").lower()

# # Calculos base
# cargo_fijo = 7000
# costo_por_m3 = 200
# costo_consumo = consumo * costo_por_m3
# subtotal_base = cargo_fijo + costo_consumo

# # Inicializar variables para ajustes
# bonificacion = 0
# recargo = 0
# descuento_especial = 0

# # Aplicar reglas según tipo de cliente
# if tipo_cliente == "residencial":
#     if consumo < 30:
#         bonificacion = costo_consumo * 0.10
#     if consumo > 80:
#         recargo = costo_consumo * 0.15
#     if subtotal_base < 35000:
#         descuento_especial = subtotal_base * 0.05

# elif tipo_cliente == "comercial":
#     if consumo > 300:
#         bonificacion = costo_consumo * 0.12
#     elif consumo > 150:
#         bonificacion = costo_consumo * 0.08
#     if consumo < 50:
#         recargo = costo_consumo * 0.05

# elif tipo_cliente == "industrial":
#     if consumo > 1000:
#         bonificacion = costo_consumo * 0.30
#     elif consumo > 500:
#         bonificacion = costo_consumo * 0.20
#     if consumo < 200:
#         recargo = costo_consumo * 0.10

# else:
#     print("ERROR: Tipo de cliente no valido. Use: Residencial, Comercial o Industrial")
#     exit()

# # Calculos finales
# subtotal_con_ajustes = subtotal_base - bonificacion + recargo - descuento_especial
# iva = subtotal_con_ajustes * 0.21
# total_pagar = subtotal_con_ajustes + iva

# # Mostrar resultados
# print("\n" + "="*50)
# print("DETALLE DE FACTURA")
# print("="*50)
# print(f"Tipo de cliente: {tipo_cliente.title()}")
# print(f"Consumo: {consumo} m³")
# print(f"Cargo fijo: ${cargo_fijo:,.2f}")
# print(f"Costo por consumo: ${costo_consumo:,.2f}")
# print(f"Subtotal base: ${subtotal_base:,.2f}")

# if bonificacion > 0:
#     print(f"Bonificación: -${bonificacion:,.2f}")
# if recargo > 0:
#     print(f"Recargo: +${recargo:,.2f}")
# if descuento_especial > 0:
#     print(f"Descuento especial: -${descuento_especial:,.2f}")

# print(f"Subtotal con ajustes: ${subtotal_con_ajustes:,.2f}")
# print(f"IVA (21%): ${iva:,.2f}")
# print("="*50)
# print(f"TOTAL A PAGAR: ${total_pagar:,.2f}")
# print("="*50)

# ===========================================================

# #Ingreso de datos
# metrosconsum = int(input("Ingrese la cantidad de metros consumidos: "))
# tp = input("Ingrese que tipo de cliente es: Residencial, Comercial o Industrial: ")


# if tp not in ["Residencial", "Comercial", "Industrial"]:
#     print("Tipo de cliente invalido. Debe ser Residencial, Comercial o Industrial.")
#     exit()

# print("="*50)
# print(f"Cantidad de metros consumidos: {metrosconsum}m³")
# print(f"Tipo de cliente: {tp}")
# print("="*50)

# #Calculos
# #Subtotal
# cargo_fijo = 7000
# costo_mt = 200


# subtotal = cargo_fijo + (metrosconsum * costo_mt)

# print("="*50)
# print(f"Subtotal: ${subtotal}")
# print("="*50)

# #Bonificaciones
# bonificacion = 0
# recargo = 0


# if tp == "Residencial":
#     if metrosconsum < 30 :
#         bonificacion = 0.10
#     elif metrosconsum > 80:
#         recargo = 0.15
# elif tp == "Comercial":
#     if metrosconsum > 300 :
#         bonificacion = 0.12
#     elif metrosconsum > 150 :
#         bonificacion = 0.08
#     elif metrosconsum < 50 :
#         recargo = 0.05
# elif tp == "Industrial" :
#     if metrosconsum > 1000 :
#         bonificacion = 0.30
#     elif metrosconsum > 500 :
#         bonificacion = 0.20
#     elif metrosconsum < 200 :
#         recargo = 0.10


# #Aplicación de bonifiaciones y recargos
# if bonificacion > 0 :
#     subtotal = subtotal - (subtotal * bonificacion)


# if recargo > 0 :
#     subtotal = subtotal + (subtotal * recargo)

# print("="*50)
# print(f"Bonificacion aplicada: {bonificacion * 100}%")
# print(f"Recargo aplicado: {recargo * 100}%")
# print(f"Subtotal con bonificaciones o  recargos aplicados: ${subtotal}")


# #Iva y bonificacion especial
# bonificacion_extra = 0


# if tp == "Residencial" and bonificacion <= 0 and recargo <=0 and subtotal < 35000 :
#     bonificacion_extra = 0.05
#     subtotal = subtotal - (subtotal * bonificacion_extra)

# Iva = subtotal * 0.21
# Total_final = subtotal + Iva

# print("="*50)
# print(f"Bonificacion especial aplicada: {bonificacion_extra * 100}%")
# print(f"Iva aplicado(21%): ${Iva}")
# print(f"Total final a pagar: ${Total_final}")

# ====================================================================
# #INPUT DEL CLIENTE
# cantidadMetrosConsu = int(input("Por favor ingrese el consumo de metros que tuvo: "))
# tipoCliente = input("Por favor ingrese su tipo de cliente(Residencial, Comercial o Industrial.): ").lower()

# #PIDE ENUNCIADO
# cargoFijo = 7000
# costoMetro = 200 * cantidadMetrosConsu

# #VARIABLES
# recargo= "No hay recargo."
# bonificacion = "No hay bonificacion"
# casoEspecial = ""

# match tipoCliente:
#     case "residencial":
#         if cantidadMetrosConsu < 30:
#             costoMetro -= costoMetro * 0.10
#             bonificacion = "Bonificacion del 10%"
#         elif cantidadMetrosConsu > 80:
#             costoMetro += costoMetro * 0.15
#             recargo = "Recargo del 15%"
#     case "comercial":
#         if cantidadMetrosConsu > 300:
#             costoMetro -= costoMetro * 0.12
#             bonificacion = "Bonificacion del 12%"
#         elif cantidadMetrosConsu > 150:
#             costoMetro -= costoMetro * 0.08
#             bonificacion = "Bonificacion del 8%"
#         elif cantidadMetrosConsu < 50:
#             costoMetro += costoMetro * 0.05
#             recargo = "Recargo del 5%"
#     case "industrial":
#         if cantidadMetrosConsu > 1000:
#             costoMetro -= costoMetro * 0.30
#             bonificacion = "Bonificacion del 30%"
#         elif cantidadMetrosConsu > 500:
#             costoMetro -= costoMetro * 0.20
#             bonificacion = "Bonificacion del 20%"
#         elif cantidadMetrosConsu < 200:
#             costoMetro += costoMetro * 0.10
#             recargo = "Recargo del 10%"

# if tipoCliente == "residencial" and costoMetro < 35000:
#     costoMetro -= costoMetro * 0.05
#     casoEspecial = "Se le adiciona un 5% de descuento"

# subtotalSinNada = 200 * cantidadMetrosConsu #ta bien
# subtotal = costoMetro + cargoFijo
# iva = subtotal * 0.21
# total = subtotal + iva

# print(f"Su subtotal de consumo sin bonificaciones ni recargo es de ${subtotalSinNada}") #Ta bien
# print("======================================")
# print(f"Su subtotal con bonificaciones o recargos es de ${subtotal}")
# print("======================================")


# if casoEspecial:
#     print(f" {bonificacion} {casoEspecial}")
# else:
#     print(f"{bonificacion}")
# print("======================================")

# print(f"{recargo}")
# print("======================================")

# print (f"IVA aplicacion sin bonificaciones ni recargo es del ${iva}")
# print("======================================")
# print(f"El monto final a pagar es de ${total} ")

# metros_consumidos = int(input("ingrese una cantidad de metros: "))
# cliente = input("ingrese el tipo de cliente(Residencial, Comercial o Industrial): ")
# subtotal = (metros_consumidos * 200) + 7000
# iva = (subtotal * 0.21)
# bonificacion = 0
# recargo = 0
# subtotal_final = 0

# match cliente:
#     case "Residencial":
#         if metros_consumidos < 30:
#             bonificacion = (subtotal * 0.1)
#         elif metros_consumidos > 80:
#             recargo = (subtotal * 0.15)
# ########################################################
#     case "Comercial":
#         if metros_consumidos > 150:
#             bonificacion = (subtotal * 0.08)
#         elif metros_consumidos > 300:
#             bonificacion = (subtotal * 0.12)
#         elif metros_consumidos < 50:
#             recargo = (subtotal * 0.05)        
# ########################################################    
#     case "Industrial":
#         if metros_consumidos > 500:
#             bonificacion = (subtotal * 0.20)
#         elif metros_consumidos > 1000:
#             bonificacion = (subtotal * 0.30)
#         elif metros_consumidos < 200:
#             recargo = (subtotal * 0.10)

# if subtotal > 35000 and cliente == "Residencial":
#     subtotal_final = subtotal - (subtotal * 0.05)


# subtotal_final =+ subtotal + recargo - bonificacion + iva

# print(f"""
#       Por {metros_consumidos} m3
#       metros se debe pagar: ${subtotal},
#       Al ser cliente {cliente}, 
#       posee un recargo de ${recargo}  
#       El IVA aplicado es de ${iva}
#       y una bonificacion de ${bonificacion}, 
#       por lo tanto su subtotal es: ${subtotal_final}
#       """)
