from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models, database
from database import engine
from passlib.context import CryptContext

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Tareas", version="1.0")

# Seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración CORS (para conectar con React)
// src/api.js o donde configures Axios
import axios from "axios";

const API_URL = "https://proyecto-final-backend-1nh4.onrender.com";

export const api = axios.create({
  baseURL: API_URL,
});


# ---- Modelos Pydantic ----
class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TareaRequest(BaseModel):
    titulo: str
    descripcion: str


@app.get("/")
def raiz():
    return {"mensaje": "API de tareas activa ✅"}


# ---- Registro ----
@app.post("/register")
def register_user(data: RegisterRequest, db: Session = Depends(database.get_db)):
    if len(data.password) > 72:
        raise HTTPException(status_code=400, detail="La contraseña no puede tener más de 72 caracteres")

    user = db.query(models.User).filter(models.User.username == data.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    hashed_password = pwd_context.hash(data.password[:72])  # recorta si es necesario
    new_user = models.User(username=data.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuario registrado correctamente"}


# ---- Login ----
@app.post("/login")
def login_user(data: LoginRequest, db: Session = Depends(database.get_db)):
    username = data.username.strip()
    password = data.password.strip()

    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    return {"message": "Login exitoso ✅"}


# ---- Tareas ----
@app.get("/tareas")
def obtener_tareas(db: Session = Depends(database.get_db)):
    return db.query(models.Tarea).all()


@app.post("/tareas")
def crear_tarea(data: TareaRequest, db: Session = Depends(database.get_db)):
    nueva_tarea = models.Tarea(titulo=data.titulo.strip(), descripcion=data.descripcion.strip())
    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea)
    return nueva_tarea


@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int, db: Session = Depends(database.get_db)):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(tarea)
    db.commit()
    return {"message": "Tarea eliminada correctamente ✅"}
