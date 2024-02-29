from fastapi import APIRouter, FastAPI,Depends,status,Response
from fastapi.security import HTTPBearer
from core import get_db
from sqlalchemy.orm import Session
from core.database import SessionLocal
from crud.subcategories import get_subcate
from models import schemas
import models as model

async def statistica(static:schemas.QuestionLen,db: Session = Depends(get_db)):
    question =await get_subcate(db=db)
    
    # blog.append()
    return question
async def create_statisc(req: model.QuestionLen, db: Session = Depends(get_db)):
    new_add = model.QuestionLenght(**req.dict())
    
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add