from fastapi import APIRouter, FastAPI,Depends, HTTPException, Request,status,Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from core import get_db
from sqlalchemy.orm import Session
from core.auth import authenticate_admin, get_current_user
import crud
import models as mod


info = APIRouter(
    prefix='/information',
    # dependencies=[Depends(HTTPBearer())],
    tags=['information']
)


@info.get('/get_subcategories',status_code=status.HTTP_200_OK)
async def get_categories(db: Session = Depends(get_db),):
    data=await crud.info_get(db)
    result =  data
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#----------------------------------------------------------------------------------
@info.post('/add_information')
async def post_categoies(req: mod.Info, db: Session = Depends(get_db)):   
    result = await crud.create_info(req, db)
    if result:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#------------------------------------------------------------
@info.delete("/delete_categories/{id}", status_code=status.HTTP_200_OK,dependencies=[Depends(HTTPBearer())])
async def delete_cate(id:int,header_param: Request,db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    check_delete= await crud.delete_info(id=id,db=db)
    if(check_delete):
        return JSONResponse(content={"info":"Sucessed"}, status_code=status.HTTP_201_CREATED)
    else:
       return JSONResponse(content={"info":"Unsucessed"}, status_code=status.HTTP_400_BAD_REQUEST)
#-------------------------------------------------------------------------------------------------------------------------
@info.put("/change_categories/{id}", status_code=status.HTTP_200_OK,dependencies=[Depends(HTTPBearer())])
async def change_cateogies(id:int,req: mod.Info,header_param: Request,db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    change_data=await crud.update_info(id=id,req=req,db=db)
    if change_data==1:
        return JSONResponse(content={"info":"Sucessed"}, status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={"info":"Unsucessed"}, status_code=status.HTTP_400_BAD_REQUEST)
    
    