from fastapi import APIRouter, FastAPI,Depends, HTTPException, Request,status,Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from core import get_db
from sqlalchemy.orm import Session
from core.auth import authenticate_admin, get_current_user
import crud
import models as mod


category = APIRouter(
    prefix='/categories',
    # dependencies=[Depends(HTTPBearer())],
    tags=['categories']
)


@category.get('/get_subcategories',status_code=status.HTTP_200_OK)
async def get_info(db: Session = Depends(get_db),):
    data=await crud.home(db)
    result =  {"categories":data,"len":len(data) }
    print(data)
    
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#----------------------------------------------------------------------------------
@category.post('/add_categories', dependencies=[Depends(HTTPBearer())])
async def post_info(req: mod.Blogs, header_param: Request,db: Session = Depends(get_db)):   
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    result = await crud.create_blog(req, db)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#--------------------------------------------
@category.delete("/delete_categories/{id}", status_code=status.HTTP_200_OK,dependencies=[Depends(HTTPBearer())])
async def delete_cate(id:int,header_param: Request,db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    check_delete= await crud.delete_cat(id=id,db=db)
    if(check_delete):
        return JSONResponse(content={"info":"Sucessed"}, status_code=status.HTTP_201_CREATED)
    else:
       return JSONResponse(content={"info":"Unsucessed"}, status_code=status.HTTP_400_BAD_REQUEST)
#---------------------------------------------------------------
@category.put("/change_categories/{id}", status_code=status.HTTP_200_OK,dependencies=[Depends(HTTPBearer())])
async def change_cateogies(id:int,req: mod.Blogs,header_param: Request,db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    change_data=await crud.update_data(id=id,req=req,db=db)
    if change_data==1:
        return JSONResponse(content={"info":"Sucessed"}, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={"info":"Unsucessed"}, status_code=status.HTTP_400_BAD_REQUEST)
    
    