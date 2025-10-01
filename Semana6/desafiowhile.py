# # Encuesta Tecnológica - UTN Technologies
# """
# Validación de datos:
# Nombre no vacío.
# Edad numérica ≥ 18.
# Género solo “Masculino/Femenino/Otro”.
# Tecnología solo “IA/RV/RA/IOT”, unificando RV y RA como “RV/RA”.

# Métricas:
# M1: Hombres que votaron IA o IOT, con edad 25–50.
# M2: Porcentaje de quienes no votaron IA, no son femeninos, edad 33–40.
# M3: Hombre de mayor edad, mostrando nombre y tecnología.
# Salida:
# Imprime los resultados en forma clara, incluso cuando no se cumplen condiciones para alguna métrica.
# """
# TOTAL = 10

# # --- Contadores y variables para métricas ---
# cont_masc_iot_ia_25_50 = 0
# cont_no_ia_condiciones = 0
# cont_total_condiciones = 0
# mayor_edad_masc = -1
# nombre_mayor_masc = ""
# tecno_mayor_masc = ""

# for i in range(1, TOTAL + 1):
#     print(f"\n--- Empleado {i} ---")

#     # Validar nombre
#     while True:
#         nombre = input("Nombre: ").strip()
#         if nombre:
#             break
#         print("❗ El nombre no puede estar vacío.")

#     # Validar edad
#     while True:
#         try:
#             edad = int(input("Edad (>=18): "))
#             if edad >= 18:
#                 break
#             else:
#                 print("❗ La edad debe ser 18 o mayor.")
#         except ValueError:
#             print("❗ Ingrese un número válido para la edad.")

#     # Validar género
#     while True:
#         genero = input("Género (Masculino/Femenino/Otro): ").strip().lower()
#         if genero in ["masculino", "femenino", "otro"]:
#             break
#         print("❗ Género inválido.")

#     # Validar tecnología
#     while True:
#         tecnologia = input("Tecnología (IA/RV/RA/IOT): ").strip().upper()
#         if tecnologia in ["IA", "RV", "RA", "IOT"]:
#             # Unificar RV y RA en un solo valor para consistencia
#             if tecnologia == "RV" or tecnologia == "RA":
#                 tecnologia = "RV/RA"
#             break
#         print("❗ Tecnología inválida. Use IA, RV, RA o IOT.")

#     # --- Métrica 1 ---
#     if genero == "masculino" and 25 <= edad <= 50 and tecnologia in ["IA", "IOT"]:
#         cont_masc_iot_ia_25_50 += 1

#     # --- Métrica 2 ---
#     if genero != "femenino" and 33 <= edad <= 40:
#         cont_total_condiciones += 1
#         if tecnologia != "IA":
#             cont_no_ia_condiciones += 1

#     # --- Métrica 3 ---
#     if genero == "masculino" and edad > mayor_edad_masc:
#         mayor_edad_masc = edad
#         nombre_mayor_masc = nombre
#         tecno_mayor_masc = tecnologia

# # --- Resultados ---
# print("\n===== RESULTADOS DE LA ENCUESTA =====")
# print(f"1 Cantidad de hombres que votaron IA/IOT y tienen entre 25 y 50 años: {cont_masc_iot_ia_25_50}")

# if cont_total_condiciones > 0:
#     porcentaje = (cont_no_ia_condiciones / cont_total_condiciones) * 100
#     print(f"2 Porcentaje de empleados (género ≠ Femenino, edad 33-40) que NO votaron IA: {porcentaje:.2f}%")
# else:
#     print("2 No hubo empleados que cumplieran las condiciones para calcular el porcentaje.")

# if mayor_edad_masc >= 0:
#     print(f"3 Empleado masculino de mayor edad: {nombre_mayor_masc} ({mayor_edad_masc} años) - Tecnología: {tecno_mayor_masc}")
# else:
#     print("3 No se ingresaron empleados masculinos.")


# # ==============================1==============================

# EMPLEADOS = 5
# generos = ['masculino', 'femenino', 'otro']
# tecnologias = ['IA', 'RV/RA', 'RV', 'RA', 'IOT']
# respuestas = edad = 0
# nombre = genero = tecnologia = ''
# empleados_masculinos_IOT_IA_25_50 = 0
# empleados_no_femeninos_noIA_33_40 = 0
# edad_empleado_mayor = 0
# nombre_empleado_mayor = tecnologia_empleado_mayor = ''


# while respuestas < EMPLEADOS:
    
#     # Ingreso del nombre
#     while True:
#         nombre = input('Ingrese nombre: ').lower()
#         if nombre.isalpha():
#             break
#         print('Error. El nombre solo debe contener letras')

#     # Ingreso de la edad   
#     while True:
#         edad = int(input('Ingrese edad: '))
#         if 17 < edad < 90:
#             break
#         print('Error. La edad debe estar entre 18 y 90 años')

#     # Ingreso del género          
#     while True:
#         genero = input('Ingrese género (maculino, femenino, otro): ').lower()
#         if genero in generos:
#             break
#         print('Error. El género debe ser "Masculino, Femenino, Otro"')
        
#     # Ingreso de la tecnologia          
#     while True:
#         tecnologia = input('Ingrese tecnologia (IA, RV/RA, IOT): ').upper()
#         if tecnologia in tecnologias:
#             break
#         print('Error. La tecnología debe ser: "IA", "RV/RA", "IOT"')


#     # Cantidad de emplados masculinos que votaron por IA o IOT (entre 25 y 50)
#     if genero == 'masculino' and 25 < edad < 50 and tecnologia in ['IA', 'IOT']:
#         empleados_masculinos_IOT_IA_25_50 += 1
    
#     # Calcular % de empleados que no votaron por IA (no femenino. Entre 33 y 40 años)
#     if genero != 'femenino' and 32 < edad < 41 and tecnologia != 'IA':
#         empleados_no_femeninos_noIA_33_40 += 1
    
#     # Información del empleado mayor
#     if genero == 'masculino' and edad > edad_empleado_mayor:
#         edad_empleado_mayor = edad
#         nombre_empleado_mayor = nombre
#         tecnologia_empleado_mayor = tecnologia

#     respuestas += 1
    
# print(f"""
#       Resultados
#       {80*'='}
#       Cantidad de emplados masculinos que votaron por IA o IOT (entre 25 y 50): {empleados_masculinos_IOT_IA_25_50}
#       Porcentaje de empleados que no votaron por IA (no femenino. Entre 33 y 40 años): %{(empleados_no_femeninos_noIA_33_40 / EMPLEADOS) * 100}
#       Empleado mayor: {nombre_empleado_mayor.capitalize()} votó por {tecnologia_empleado_mayor} y tiene {edad_empleado_mayor} años
#         """)

# =====================================================================
# CANTIDAD DE ENTREVISTADOS
# cantIngresos = 0
# #VOTOS DE LOS ENTREVISTADOS
# votosPorIA = 0
# votosPorIOT = 0
# votosPorRV = 0
# notVotosIA = 0

# #PERSONA CON MAYOR EDAD
# edadMayor = 0
# nombreMayor = "El nombre de la persona con mayor edad"
# tecnologíaMayor = "Tecnologia elegida del mayor de edad"

# while not (cantIngresos == 6) :
   
#     #INPUTS PARA LOS DATOS DEL EMPLEADO
#     nombre = input("Por favor ingrese su nombre: ")
#     edad = int(input("Ingrese su edad(debe ser 18 años o más): ")) #(debe ser 18 años o más)
#     genero = input("Por favor ingrese su genero: ").lower() #(Masculino, Femenino, Otro)
#     tecnologíaElegida = input('Ingrese la tecnologia elegida ("IA", "RV/RA", "IOT"): ') #(IA, RV/RA, IOT)
   
#     #MATCH PARA CASO DE GENERO
#     match genero :
#         case "masculino":
#             #MASCULINOS QUE VOTARON POR IA O IOT
#             if tecnologíaElegida != "RV/RA" and 25 <= edad <= 50:
#                 match tecnologíaElegida:
#                     case "IA":
#                         votosPorIA += 1
#                     case "IOT":
#                         votosPorIOT += 1
#             elif 33 <= edad <= 40:    #MASCULINOS QUE NO VOTARON POR IA
#                 notVotosIA += 1
#                 if tecnologíaElegida == "IOT":
#                     votosPorIOT += 1
#                 elif tecnologíaElegida == "RV/RA":
#                     votosPorRV +=1
#     if edad > edadMayor:
#         edadMayor = edad
#         nombreMayor = nombre
#         tecnologíaMayor = tecnologíaElegida
       
#     cantIngresos += 1


# #PORCENTAJES DE VOTOS
# porcentajeVotosPorIA = (votosPorIA / cantIngresos) * 100
# porcentajeVotosPorIOT = (votosPorIOT / cantIngresos) * 100
# porcentajeVotosPorRVRA = (votosPorRV / cantIngresos) * 100
# porcentajeVotosQueNoFueronParaIA = (notVotosIA / cantIngresos) * 100


# #PRINTS DE VOTOS Y LA PERSONA DE MAYOR EDAD
# print(f"El porcentaje de votos por IA es de {porcentajeVotosPorIA}")
# print("======================================")
# print(f"El porcentaje de votos por IOT es de {porcentajeVotosPorIOT}")
# print("======================================")
# print(f"El porcentaje de votos por RV/RA es de {porcentajeVotosPorRVRA}")
# print("======================================")
# print(f"El porcentaje de empleados masculinos, con edad entre 33 y 40 años que no votaron por IA es de {porcentajeVotosQueNoFueronParaIA}")
# print("======================================")
# print(f"El nombre de la persona con mas edad es {nombreMayor}, su edad es de {edadMayor} y voto por la tecnologia de {tecnologíaMayor}")

# ====================================================================

# votos_masculinos = 0
# contador_empleado = 0
# voto_empleado_no_ia = 0
# bandera = True


# while contador_empleado < 3: #EN REALIDAD ME PIDEN 10 EMPLEADOS. PUSE 3 PARA PROBAR
#     nombre = input("INGRESE SU NOMBRE: ")


#     edad = int(input("INGRESE SU EDAD. DEBE SER MAYOR DE 18 AÑOS: "))
#     while edad < 18 or edad > 140:
#         edad = int(input("REINGRESE SU EDAD. DEBE SER MAYOR DE 18 AÑOS: "))


#     genero = input("INGRESE SU GENERO MASCULINO, FEMENINO, OTRO: ")
#     while genero != "MASCULINO" and genero != "OTRO" and genero != "FEMENINO":
#         genero = input("REINGRESE SU GENERO MASCULINO, FEMENINO, OTRO: ")


#     tecnologia_elegida = input("INGRESA EL TIPO DE TECNOLOGIA... IA, RV/RA, IOT: ")
#     while tecnologia_elegida != "IA" and tecnologia_elegida != "RV" and tecnologia_elegida != "RA" and tecnologia_elegida != "IOT":
#         tecnologia_elegida = input("REINGRESA EL TIPO DE TECNOLOGIA... IA, RV/RA, IOT: ")
   
#     contador_empleado += 1
   
#     if tecnologia_elegida != "IA":
#         if edad > 32 and edad < 41:
#             if genero != "FEMENINO":
#                 voto_empleado_no_ia += 1


   
#     if genero == "MASCULINO":
#         if tecnologia_elegida == "IA" or tecnologia_elegida == "IOT":
#             if edad > 24 and edad < 51:
#                 votos_masculinos += 1
#         if bandera == True: # EL PRIMER MASCULINO SERA EL MAS GRANDE HASTA QUE LO COMPARE CON EL SIGUIENTE
#             edad_max = edad
#             nombre_masculino_mayor = nombre
#             voto_masculino_mayor = tecnologia_elegida
#             bandera = False # CAMBIO EL ESTADO DE BANDERA PARA QUE A LOS SIGUIENTES LOS COMPARE
#         else:
#             if edad > edad_max:
#                 edad_max = edad
#                 nombre_masculino_mayor = nombre
#                 voto_masculino_mayor = tecnologia_elegida






# porcetaje_votos_no_ia = (voto_empleado_no_ia * 100) / contador_empleado


# #respuesta 1
# print(f"La cantidad de empleados de género masculino que votaron por IOT o IA, cuya edad esté entre 25 y 50 años (inclusive) es: {votos_masculinos}\n")


# #respuesta 2
# print(f"""Porcentaje de empleados que NO votaron por IA, siempre y cuando:
#             ●   Su género no sea Femenino
#             ●   Su edad está entre los 33 y 40 años.
#       EL PORCETAJE ES IGUAL A: {porcetaje_votos_no_ia}%\n""")


# #respuesta 3
# print(f"El hombre de mayor edad es: {nombre_masculino_mayor}\nVoto por la tecnologia {voto_masculino_mayor}\nTiene {edad_max} años de edad\n")        

# ____________________________________________________________
TOTAL_EMPLEADOS = 5
contador = 0
nombre_masculino_mayor= ""
edad_mas_grande = 0
tecnologia_del_mayor = ""

cant_no_voto_ia = 0
cant_voto_iot_ia = 0

while contador != TOTAL_EMPLEADOS:
    contador += 1
   
    nombre = input("Ingrese su nombre: ")
    edad = int(input("Ingrese su edad(+18): "))
    while edad < 18:
        edad = int(input("Porfavor ingrese una edad válida(+18): "))


    genero = input("Ingrese su Género(hombre/mujer): ")
    while genero != "hombre" and genero != "mujer":
        genero = input("Porfavor ingrese genero válido(hombre/mujer): ")


    tecnologia =  input("ingrese una tecnologia(IA, RV/RA, IOT): ")
    while tecnologia != "IA" and tecnologia != "IOT" and tecnologia != "RV/RA":
        tecnologia = input("Porfavor ingrese una tecnologia válida(IA, RV/RA, IOT): ")


    if genero == "hombre":
        match tecnologia:
            case "IOT":
                if (edad >= 25 and edad <= 50):
                    cant_voto_iot_ia += 1
                if (edad >= 33 and edad <= 40):
                    cant_no_voto_ia += 1
            case "IA":
                if (edad >= 25 and edad <= 50):
                    cant_voto_iot_ia += 1


            case "RV/RA":
                if (edad >= 33 and edad <= 40):
                    cant_no_voto_ia += 1
       
        if edad > edad_mas_grande:
            edad_mas_grande = edad
            nombre_masculino_mayor = nombre
            tecnologia_del_mayor = tecnologia
    print(f"empleados ingresados hasta ahora({contador})")


porcentaje_no_votaron_ia = (cant_no_voto_ia / TOTAL_EMPLEADOS) * 100
print(f"""
    Empleados hombres que votaron por IOT/IA, entre 33 y 40 años: {cant_voto_iot_ia}.
    Empleados hombres que NO votaron por IA, entre 25 y 50 años es un porcentaje de: {porcentaje_no_votaron_ia}.
    El empleado hombre mas antiguo es {nombre_masculino_mayor} y su tecnologia votada fue {tecnologia_del_mayor}""")
   

