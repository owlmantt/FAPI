from datetime import timedelta
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models
import security
from database import engine, get_db
from pydantic import BaseModel

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Схемы Pydantic
class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str
    role: str

    class Config:
        orm_mode = True

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

# Эндпоинты для аутентификации
@app.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# CRUD операции для заметок
@app.post("/notes/", response_model=Note)
def create_note(
    note: NoteCreate,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    db_note = models.Note(**note.dict(), owner_id=current_user.id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.get("/notes/", response_model=List[Note])
def read_notes(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    notes = db.query(models.Note).filter(models.Note.owner_id == current_user.id).offset(skip).limit(limit).all()
    return notes

@app.get("/notes/{note_id}", response_model=Note)
def read_note(
    note_id: int,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.put("/notes/{note_id}", response_model=Note)
def update_note(
    note_id: int,
    note: NoteUpdate,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    db_note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    for key, value in note.dict().items():
        setattr(db_note, key, value)
    
    db.commit()
    db.refresh(db_note)
    return db_note

@app.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}