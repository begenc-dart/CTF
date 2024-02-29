from fastapi import Depends, File
from sqlalchemy.orm import Session
from core.database import get_db
from crud.image import delete_uploaded_image, upload_image
from models.model import Subcategories


async def update_post_image( id:int, file,db: Session = Depends(get_db)):
    print(str(id)+"dsadsa")
    get_image = db.query(Subcategories).filter(Subcategories.id == id).first()
    
    db.close()
    print(get_image.answer)
    if get_image.file is not None:
        try:
            delete_uploaded_image(image_name=get_image.file)
        except Exception as e:
            print(e)
    uploaded_img = upload_image(directory="posts", file=file)
    
    new_update = db.query(Subcategories).filter(Subcategories.id == id).\
        update({
            Subcategories.file : uploaded_img
        }, synchronize_session=False)
    
    data=get_image.file
    print(data)
    db.commit()
    db.close()
    if new_update:
        return data
    else:
        return None