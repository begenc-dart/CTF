from pydantic import BaseModel


class Blogs(BaseModel):
    categories_name: str
class SubCategor_model(BaseModel):
    point:int
    # done:int
    categorid:int
    name:str
    answer:str
    question:str
class LoginShema(BaseModel):
    # student_id: int
    name:str
    surname:str
    username:str
    pasword:str
class Info(BaseModel):
    title:str
    subtitle:str
class Sigin(BaseModel):
    username:str
    password:str
class QuestionCheck(BaseModel):
    userId:int
    taskId:int
    solition:bool

    

   