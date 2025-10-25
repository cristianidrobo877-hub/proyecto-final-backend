from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crear_tarea():
    respuesta = client.post("/tareas", json={"titulo": "Prueba", "descripcion": "Testing", "completada": False})
    assert respuesta.status_code == 200
    assert respuesta.json()["titulo"] == "Prueba"

def test_listar_tareas():
    respuesta = client.get("/tareas")
    assert respuesta.status_code == 200
    assert type(respuesta.json()) is list
