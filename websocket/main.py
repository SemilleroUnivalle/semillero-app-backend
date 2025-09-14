from fastapi import FastAPI, WebSocket, Depends, Query
from db import SessionLocal, engine
from Asistencia.models import Base, Asistencia
from sqlalchemy.orm import Session
import json
from typing import List

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

active_connections = []

@app.websocket("/ws/asistencia")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            # Espera {"estudiante": "Juan", "curso": "Math"}
            asistencia = Asistencia(estudiante=msg["estudiante"], curso=msg["curso"])
            db.add(asistencia)
            db.commit()
            db.refresh(asistencia)
            # Obtener todas las asistencias
            asistencias = db.query(Asistencia).all()
            asistencias_data = [
                {"id": a.id, "estudiante": a.estudiante, "curso": a.curso}
                for a in asistencias
            ]
                # Enviar la lista actualizada a todos los clientes conectados
            for conn in active_connections:
                await conn.send_text(json.dumps(asistencias_data))
    except Exception:
        pass
    finally:
        active_connections.remove(websocket)
        
        
        
