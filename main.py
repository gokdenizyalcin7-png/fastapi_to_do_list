from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

# Uygulama başladığında modelleri (tabloları) SQLite içinde otomatik oluşturur
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Veritabanı oturumunu güvenli açıp kapatan yardımcı fonksiyon (Dependency)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Task Manager API Çalışıyor!"}

@app.post("/tasks/")
def create_task(name: str, description: str, db: Session = Depends(get_db)):
    
    new_task = models.Task(name=name, description=description)
    
    
    db.add(new_task)
    
    db.commit()
    
    db.refresh(new_task)
    
    return {
        "status": "success",
        "message": "Görev başarıyla oluşturuldu",
        "data": new_task
    }