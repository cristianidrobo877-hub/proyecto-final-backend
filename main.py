from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models, database
from database import engine, get_db
from passlib.context import CryptContext

# Crear las tablas si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Tareas", version="1.0")

# Seguridad (hash de contraseñas)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# CORS: permitir solo tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://proyecto-final-frontend-tau-ochre.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

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

# ---- Endpoints ----
@app.get("/")
def raiz():
    return {"mensaje": "API de tareas activa ✅"}

# Registro de usuario
@app.post("/register")
def register_user(data: RegisterRequest, db: Session = Depends(get_db)):
    if len(data.password) > 72:
        raise HTTPException(status_code=400, detail="La contraseña no puede tener más de 72 caracteres")
    user = db.query(models.User).filter(models.User.username == data.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    hashed_password = pwd_context.hash(data.password[:72])
    new_user = models.User(username=data.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuario registrado correctamente ✅"}

# Login de usuario
@app.post("/login")
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    username = data.username.strip()
    password = data.password.strip()
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    return {"message": "Login exitoso ✅"}

# Obtener todas las tareas
@app.get("/tareas")
def obtener_tareas(db: Session = Depends(get_db)):
    return db.query(models.Tarea).all()

# Crear tarea
@app.post("/tareas")
def crear_tarea(data: TareaRequest, db: Session = Depends(get_db)):
    nueva_tarea = models.Tarea(titulo=data.titulo.strip(), descripcion=data.descripcion.strip())
    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea)
    return nueva_tarea

# Eliminar tarea
@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(tarea)
    db.commit()
    return {"message": "Tarea eliminada correctamente ✅"}
