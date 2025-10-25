import requests  

API_URL = "http://127.0.0.1:8000"

def mostrar_menu():
    print("\n--- APP DE TAREAS ---")
    print("1. Ver tareas")
    print("2. Crear tarea")
    print("3. Actualizar tarea")
    print("4. Eliminar tarea")
    print("5. Salir")

while True:
    mostrar_menu()
    opcion = input("Elige una opción: ")

    if opcion == "1":
        r = requests.get(f"{API_URL}/tareas")
        print(r.json())

    elif opcion == "2":
        titulo = input("Título: ")
        desc = input("Descripción: ")
        data = {"titulo": titulo, "descripcion": desc, "completada": False}
        r = requests.post(f"{API_URL}/tareas", json=data)
        print(r.json())

    elif opcion == "3":
        id_tarea = input("ID de la tarea a actualizar: ")
        titulo = input("Nuevo título: ")
        desc = input("Nueva descripción: ")
        data = {"titulo": titulo, "descripcion": desc, "completada": False}
        r = requests.put(f"{API_URL}/tareas/{id_tarea}", json=data)
        print(r.json())

    elif opcion == "4":
        id_tarea = input("ID de la tarea a eliminar: ")
        r = requests.delete(f"{API_URL}/tareas/{id_tarea}")
        print(r.json())

    elif opcion == "5":
        break
