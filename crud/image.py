from fastapi import File
from sqlalchemy.orm import Session
import models as _mod
import sys
import os
import uuid
import shutil

def upload_image(directory, file):
    path_const = f"/uploads/{directory}/"
    path = sys.path[0] + path_const
    print(directory+"sadsa")
    print(str(file)+"fdsfsd")
    if not os.path.exists(path):
        os.makedirs(path)
    extension = file.filename.split(".")[-1]
    unique_id = str(uuid.uuid4())
    new_name = unique_id + "." + extension
    upload_file_path_for_save_static = path + f"{new_name}"
    upload_file_path_for_db = path_const + f"{new_name}"
        
    with open(upload_file_path_for_save_static, "wb") as file_object:
        shutil.copyfileobj(file.file, file_object)
    if upload_file_path_for_db:
        return upload_file_path_for_db
    

def delete_uploaded_image(image_name):
    path_for_remove = sys.path[0] + image_name
    if os.path.exists(path_for_remove):
        os.remove(path_for_remove)

    if path_for_remove:
        return True
    
    
    
async def create(id, files, db: Session):
    for file in files:
        uploaded_image = upload_image('images', file)
        new_add = _mod.Image(
            src = uploaded_image,
            item_id = id
        )
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
    return True