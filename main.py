from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models,auth
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Security


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
def create_task(
    name: str, 
    description: str, 
    db: Session = Depends(get_db), 
    token: str = Depends(auth.oauth2_scheme) 
):
    
    new_task = models.Task(name=name, description=description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Görev başarıyla eklendi", "task": new_task}


@app.post("/register/")
def register_user(username: str, password: str, db: Session = Depends(get_db)):
    
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Kullanıcı adı zaten alınmış")
    
    
    hashed_pwd = auth.get_password_hash(password)
    new_user = models.User(username=username, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Kullanıcı başarıyla oluşturuldu"}



@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Hatalı kullanıcı adı veya şifre",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}