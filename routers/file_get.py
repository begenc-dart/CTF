


from fastapi import APIRouter, Depends, File, Request, UploadFile,status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from sqlalchemy import ReturnsRows

from sqlalchemy.orm import Session
from core.auth import authenticate_admin, get_current_user

from core.database import get_db
import crud
banner_router = APIRouter(
    prefix='/upload',
    # dependencies=[Depends(HTTPBearer())],
    tags=['upload']
)
@banner_router.put("/update-banner-image/{id}", dependencies=[Depends(HTTPBearer())])
async def update_image(id: int,header_param: Request,  files: UploadFile = File(...),db: Session = Depends(get_db)):
    
    print(id)
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    # result = await crud.update_post_image(db=db, id=id, file=files)
    try:
        print(files.filename)
        result = await crud.update_post_image(db=db, id=id, file=files)
        
        if not result:
            return "error"
        else:
            return JSONResponse(content={"url":result}, status_code=status.HTTP_201_CREATED)
    except Exception as error:
        print(error)
        return error