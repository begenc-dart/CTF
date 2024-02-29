from core import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from datetime import datetime
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__="categories"
    id=Column(Integer,primary_key=True,index=True, autoincrement=True)
    categories_name=Column(String)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)
    subcategories_len=Column(Integer,default=0)
    
    # categorya_lenght=Column(Integer,primary_key=True)
    # body=Column(String)
class Subcategories(Base):
    __tablename__="subcategor"
    id=Column(Integer,primary_key=True,index=True, autoincrement=True)
    categorid=Column(Integer)
    categories_name=Column(String)
    writer=Column(String)
    point=Column(Integer)
    file=Column(String)
    done=Column(Integer,default=0)
    name=Column(String)
    question=Column(String)
    answer=Column(String)
    check=Column(Boolean,default=False)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)
class Users(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True, autoincrement=True)
    # student_id=Column(Integer)
    name=Column(String)
    surname=Column(String)
    username=Column(String)
    pasword=Column(String)
    token = Column(String)
    point=Column(Integer,default=0)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)
class Information(Base):
    __tablename__="information"
    id=Column(Integer,primary_key=True,index=True, autoincrement=True)
    title=Column(String)
    subtitle=Column(String)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)
class CheckQuestion(Base):
    __tablename__="check"
    id=Column(Integer,primary_key=True,index=True, autoincrement=True)
    userId=Column(Integer)
    taskId=Column(Integer)
    
    solition=Column(Boolean)
