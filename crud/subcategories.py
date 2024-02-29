from fastapi import APIRouter, FastAPI,Depends,status,Response
from fastapi.security import HTTPBearer
from core import get_db
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models import schemas
from sqlalchemy import and_, or_
import models as model

async def get_subcate(offset:int, limit:int,db: Session = Depends(get_db)):
    blog = db.query(model.Subcategories).offset(offset).limit(limit).all()
    return blog

async def count_subcate(db: Session = Depends(get_db)):
    blog = db.query(model.Subcategories).count()
    return blog
# -------------------------------------------------------
async def get_categorid(id:int,db: Session = Depends(get_db)):
    blog = db.query(model.Subcategories).filter(id==model.Subcategories.categorid).all()
    return blog
#----------------------------------------------------------------
async def one_categories(id:int,db: Session = Depends(get_db)):
    blog = db.query(model.Subcategories).filter(id==model.Subcategories.id).all()
    return blog
#------------------------------------------------------------
async def categories_check(id:int,userId:int,db: Session = Depends(get_db)):
    blog = db.query(model.CheckQuestion).filter(and_(model.CheckQuestion.taskId==id , userId==model.CheckQuestion.userId)).first()
    # print(len(blog))
    return blog
#--------------------------------------------
async def checkLen(id:int,userId:int,db: Session = Depends(get_db)):
    blog = db.query(model.CheckQuestion).filter(userId==model.CheckQuestion.userId).all()
    # print(blog.solition)
    return blog
#-----------------------------------------------
async def add_checkquest(req: model.QuestionCheck,db: Session = Depends(get_db),):
    new_add = model.CheckQuestion(**req.dict() )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add
#----------------------------------------------------------------------------------------

# -------------------------------------------------------
async def add_subcate(req: model.SubCategor_model, writer:str,categoires_name:str,db: Session = Depends(get_db),):
    new_add = model.Subcategories(**req.dict() )
    new_add.writer=writer
    new_add.categories_name=categoires_name
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add
#-----------------------------------------------
async def done_count(req: model.Subcategories, db: Session = Depends(get_db),):
    db.add(req)
    db.commit()
    db.refresh(req)
    return req
#-----------------------------------------------------------
async def done_users(req: model.Users, db: Session = Depends(get_db),):
    db.add(req)
    db.commit()
    db.refresh(req)
    return req
#------------------------------------------------------------
async def get_search(search:str,db: Session = Depends(get_db)):
    blog = db.query(model.Subcategories).filter(model.Subcategories.name.like('%'+search+'%')).all()
    print()
    return blog
#-------------------------------------------------------------
async def get_usersearch(search:str,db: Session = Depends(get_db)):
    blog = db.query(model.Users).filter(model.Users.username.like('%'+search+'%')).all()
    # print()
    return blog
#------------------------------------------

async def delete_question(id:int,db: Session = Depends(get_db)):
    data=db.query(model.Subcategories)\
            .filter(model.Subcategories.id==id).delete(synchronize_session=False)
    db.commit()
    db.close()
    return True