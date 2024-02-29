from fastapi import APIRouter, FastAPI,Depends,status,Response
from fastapi.security import HTTPBearer
from core import get_db
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models import schemas
import models as model

async def info_get(db: Session = Depends(get_db)):
    blog = db.query(model.Information).all()
    # blog.append()
    return blog
async def create_info(req: model.Info, db: Session = Depends(get_db)):
    new_add = model.Information(**req.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add
async def delete_info(id:int,db: Session = Depends(get_db)):
    
    data=db.query(model.Information)\
        .filter(model.Information.id==id).delete(synchronize_session=False)
    db.commit()
    db.close()
    return True
    
async def update_info(id:int,req: model.Info, db: Session = Depends(get_db)):
    new_add = db.query(model.Information)\
        .filter(id==model.Information.id)\
            .update({
                model.Information.title:req.title,
                model.Information.subtitle:req.subtitle
            })
    # db.add(new_add)
    db.commit()
    db.close()
    return new_add
