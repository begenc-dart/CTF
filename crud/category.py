from fastapi import APIRouter, FastAPI,Depends,status,Response
from fastapi.security import HTTPBearer
from core import get_db
from sqlalchemy.orm import Session
from core.database import SessionLocal

from models import schemas
import models as model

async def home(db: Session = Depends(get_db)):
    blog = db.query(model.Blog).all()
    for i in blog:
        question=db.query(model.Subcategories).filter(i.id==model.Subcategories.categorid).count()
        
        i.subcategories_len=question
        print(i.subcategories_len)
    # blog.append()
    return blog
async def create_blog(req: model.Blogs, db: Session = Depends(get_db)):
    new_add = model.Blog(**req.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add
async def delete_cat(id:int,db: Session = Depends(get_db)):
    questionchek=db.query(model.Subcategories).filter(id==model.Subcategories.categorid).all()
    print(len(questionchek))
    if not questionchek:
        data=db.query(model.Blog)\
            .filter(model.Blog.id==id).delete(synchronize_session=False)
        db.commit()
        db.close()
        return True
    else:
        return False
async def update_data(id:int,req: model.Blogs, db: Session = Depends(get_db)):
    new_add = db.query(model.Blog)\
        .filter(id==model.Blog.id)\
            .update({
                model.Blog.categories_name:req.categories_name
            })
    # db.add(new_add)
    db.commit()
    db.close()
    return new_add