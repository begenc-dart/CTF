from fastapi import APIRouter, FastAPI,Depends, HTTPException,status,Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from core import get_db
from sqlalchemy.orm import Session
import crud
import models as mod


searchpro = APIRouter(
    prefix='/search',
    # dependencies=[Depends(HTTPBearer())],
    tags=['search']
)


@searchpro.get("/{search}")
async def get_sub(search:str,response:Response,db: Session = Depends(get_db)):
    result = await crud.get_search(search,db)
    if not result:
        response.status_code=status.HTTP_404_NOT_FOUND
        return "that id not found"
    else:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
@searchpro.get('/users_search/{search}')
async def users_search(search:str,response:Response,db: Session = Depends(get_db)):
    result = await crud.get_usersearch(search,db)
    if not result:
        response.status_code=status.HTTP_404_NOT_FOUND
        return "that id not found"
    else:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
              
# @category.post('/add_categories')
# async def post_categoies(req: mod.Blogs, db: Session = Depends(get_db)):
    
#     result = await crud.create_blog(req, db)
#     if result:
#         result = jsonable_encoder(result)
#         return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
#     else:
#         return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
