import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["1509"]
col = db["lunes"]

def mostrar_menu():
    print("\nMenú:")
    print("1. Agregar documento")
    print("2. Editar documento")
    print("3. Borrar documento")
    print("4. Listar documentos")
    print("5. Salir")

def agregar_documento():
    try:
        nombre = input("Ingrese el nombre del documento: ")
        valor = int(input("Ingrese el valor del documento: "))  # Asegurarse de que el valor sea un entero
        nuevo_documento = {"name": nombre, "value": valor}
        inserted_id = col.insert_one(nuevo_documento).inserted_id
        print(f"Documento agregado con ID: {inserted_id}")
    except ValueError:
        print("Error: El valor debe ser un número entero.")
    except Exception as e:
        print(f"Error al agregar el documento: {e}")

def editar_documento():
    try:
        id_documento = input("Ingrese el ID del documento a editar: ")
        nuevo_valor = int(input("Ingrese el nuevo valor: ")) # Asegurarse de que el valor sea un entero
        result = col.update_one({"_id": pymongo.ObjectId(id_documento)}, {"$set": {"value": nuevo_valor}})
        if result.modified_count > 0:
            print("Documento actualizado correctamente.")
        else:
            print("No se encontró ningún documento con ese ID.")
    except ValueError:
        print("Error: El valor debe ser un número entero.")
    except Exception as e:
        print(f"Error al editar el documento: {e}")


def borrar_documento():
    try:
        id_documento = input("Ingrese el ID del documento a borrar: ")
        result = col.delete_one({"_id": pymongo.ObjectId(id_documento)})
        if result.deleted_count > 0:
            print("Documento borrado correctamente.")
        else:
            print("No se encontró ningún documento con ese ID.")
    except Exception as e:
        print(f"Error al borrar el documento: {e}")

def listar_documentos():
    try:
        for doc in col.find():
            print(doc)
    except Exception as e:
        print(f"Error al listar documentos: {e}")

while True:
    mostrar_menu()
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        agregar_documento()
    elif opcion == "2":
        editar_documento()
    elif opcion == "3":
        borrar_documento()
    elif opcion == "4":
        listar_documentos()
    elif opcion == "5":
        break
    else:
        print("Opción inválida.")

client.close()
