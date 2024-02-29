from fastapi import APIRouter, FastAPI,Depends, HTTPException, Query, Request,status,Response
from fastapi import responses
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from core import get_db
from sqlalchemy.orm import Session
from core.auth import authenticate_admin, get_current_user
import crud
from crud.subcategories import add_checkquest, categories_check
import models as mod
from models.schemas import QuestionCheck


subcategor = APIRouter(
    prefix='/question',
    # dependencies=[Depends(HTTPBearer())],
    tags=['question']
)

@subcategor.get("/get_subcategories", status_code=status.HTTP_200_OK)
async def get_subcategories(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
    db: Session = Depends(get_db),
):
    # Calculate the offset based on the page and page_size
    offset = (page - 1) * page_size

    # Fetch subcategories with pagination
    result = await crud.get_subcate(db=db ,offset=offset, limit=page_size)

    # Count total number of subcategories
    total_subcategories = await crud.count_subcate(db)

    response_data = {"subcategories": result, "total_subcategories": total_subcategories, "page": page, "page_size": page_size}

    if result:
        result = jsonable_encoder(response_data)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------------------------
    
@subcategor.get("/question_host/{id}")
async def get_sub(id:int,response:Response,db: Session = Depends(get_db)):
    result = await crud.get_categorid(id,db)
    if not result:
        response.status_code=status.HTTP_404_NOT_FOUND
        return "that id not found"
    else:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#-----------------------------------------------------------------          
@subcategor.get("/question_one/{id}")
async def one_question(id:int,response:Response,db: Session = Depends(get_db)):
    result = await crud.one_categories(id,db)
    if not result:
        response.status_code=status.HTTP_404_NOT_FOUND
        return "that id not found"
    else:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#--------------------------------------------------------------------------------------------   

@subcategor.post("/add_subcategories/",status_code=200, dependencies=[Depends(HTTPBearer())])
async def show(req:mod.SubCategor_model,response:Response,header_param: Request,db:Session=Depends(get_db) ):
    
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    blog=db.query(mod.Blog).filter(mod.Blog.id==req.categorid).first()
    print(dec_token)
    if not blog:
        response.status_code=status.HTTP_404_NOT_FOUND
        return "not found"
    else:
       
        result=await crud.add_subcate(req,user.username,blog.categories_name,db)
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)
    
#----------------------------------------------------------------------
@subcategor.post("/check_answer/{id}/{answer}",status_code=200, dependencies=[Depends(HTTPBearer())])
async def check_answer(answer:str,id:int,header_param: Request,db:Session=Depends(get_db)):
    print(Request.body)
    print(id)
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    blog=db.query(mod.Subcategories).filter(id==mod.Subcategories.id).first()
    users=db.query(mod.Users).filter(user.id==mod.Users.id).first()
    check_pro= await categories_check(id=id,userId=user.id,db=db)
    
    print(str(check_pro))
    if not check_pro:
        if not blog:
            return JSONResponse(content={"data":"Your categories id is wrong"},status_code=status.HTTP_401_UNAUTHORIZED) 
        else:
            if(blog.answer==answer):
                print(answer)
                checkdata=await add_checkquest(QuestionCheck(userId=user.id,taskId=id,solition=True),db=db)
                blog.done+=1
                # blog.check=True
                users.point+=blog.point
                result= await crud.done_count(blog,db=db)
                users_count=await crud.done_users(users,db=db)
                return True
            else:
                return JSONResponse(content={"data":"Your answer is wrong"},status_code=status.HTTP_400_BAD_REQUEST) 
    else:
        return JSONResponse(content={"data":"You send question one time"},status_code=status.HTTP_403_FORBIDDEN) 
#--------------------------------------------------------------------------------------------------------
@subcategor.get("/statistica/", dependencies=[Depends(HTTPBearer())])
async def get_sub(header_param: Request,response:Response,db: Session = Depends(get_db)):
    
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    result = await crud.get_categorid(id,db)
    check= await crud.categories_check(result.id,userId=user.id,db=db)
    result.check=check
    if not result:
        response.status_code=status.HTTP_404_NOT_FOUND
        return "that id not found"
    else:
        result = jsonable_encoder(result)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
@subcategor.delete("/delete_question/{id}", status_code=status.HTTP_200_OK,dependencies=[Depends(HTTPBearer())])
async def delete_cate(id:int,header_param: Request,db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    check_delete= await crud.delete_question(id=id,db=db)
    if(check_delete):
        return JSONResponse(content={"info":"Sucessed"}, status_code=status.HTTP_201_CREATED)
    else:
       return JSONResponse(content={"info":"Unsucessed"}, status_code=status.HTTP_400_BAD_REQUEST)