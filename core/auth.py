
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import desc

from sqlalchemy.orm import Session
from starlette import status

from models.schemas import Sigin


from .database import SessionLocal, get_db
from models import Users, LoginShema
from passlib.context import CryptContext
from fastapi.security import  HTTPBearer, OAuth2PasswordBearer

# from fastapi.encoders import jsonable_encoder
from jose import jwt, JWTError

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

# class UserRequest(BaseModel):
#     username: str = 'admin'
#     password: str = 'admin'
    
    

@auth_router.get('/get-me', dependencies=[Depends(HTTPBearer())])
async def getme(header_param: Request, db:Session=Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    print(user.name)
    return db.query(Users).filter(Users.id==user.id).first()

#---------------------------------------------------------------------------

@auth_router.get('/get-users')
def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
    session: Session = Depends(get_db)
):
    # Calculate the offset based on the page and page_size
    offset = (page - 1) * page_size

    # Fetch users with pagination
    users = session.query(Users).order_by(desc(Users.point)).offset(offset).limit(page_size).all()

    # Count total number of users
    total_users = session.query(Users).count()

    result = jsonable_encoder({"users": users, "total_users": total_users, "page": page, "page_size": page_size})
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)
#----------------------------------------------------------------------
@auth_router.post('/logIn')
def  logIn(req:Sigin,session:Session=Depends(get_db)):
    user = authenticate_admin(req.username, req.password, session)
    print(req.password)
    print(req.username)
    if not user:
        return JSONResponse(content={"data":"You are not Login"}, 
                        status_code=status.HTTP_400_BAD_REQUEST) 
    else:
        return user
#----------------------------------------------------------------------- 
@auth_router.post('/create-users/', status_code=status.HTTP_201_CREATED)
async def create_user(req: LoginShema, db: Session = Depends(get_db),):
    create_user_model = Users(
        # student_id=req.student_id,
        name=req.name,
        surname=req.surname,
        username = req.username,
        pasword = bcrypt_context.hash(req.pasword),
        # group_id=req.group_id
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    access_token = create_access_token(
        req.username, 
        req.pasword, 
        create_user_model.id)
    update_user_model = db.query(Users)\
        .filter(Users.id == create_user_model.id)\
    .update({Users.token: access_token}, synchronize_session=False)
    db.commit()
    return JSONResponse(content={'token': access_token}, 
                        status_code=status.HTTP_201_CREATED)
#-----------------------------------------------------------------
def get_hashed_password(password: str) -> str:
    return bcrypt_context.hash(password)
#----------------------------------------------------------
def create_access_token(username: str, password: str, user_id: int):
    encode = {'username': username, 'password': password, 'id': user_id}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

#-------------------------------------------------------------
def authenticate_admin(username: str, password: str, db):
   
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.pasword):
        return False
    return user
#-------------------------------------------------------------
async def get_current_user(header_params: Request):
    token = header_params.headers.get('Authorization').split('Bearer ')[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('username')
        password: str = payload.get('password')
        user_id: int = payload.get('id')
        if username is None or user_id is None or password is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
        return  {
                    'username': username, 
                    'password': password, 
                    'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')