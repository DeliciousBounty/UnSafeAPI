#from datetime import datetime, timedelta
from datetime import datetime
from datetime import timedelta as delta
from optparse import TitledHelpFormatter
from sqlite3 import Date
from tkinter.tix import TEXT
from uuid import UUID
import requests
from logging.config import dictConfig
import logging
#from models import LogConfig
from typing import Any, List, Union
from fastapi.openapi.models import Server
from urllib import request, response
import uvicorn
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException,Body, status, Query
from fastapi.security import OAuth2PasswordBearer #security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#import models, schemas, crud # import the files
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse
import json
import schemas,jwt_token
from jose import jwt


#from jwt_token import JWTBearer

##in order to run  uvicorn main:app --reload

#ticket_item  = schemas.TicketInfo("9077f3ce-b852-40c0-afb1-ba04a8e5ae0c", "22/33","lorem ipsum", "lorem ipsum",5 )
#user1 = schemas.UserInfoBase("nathan","user test", "lorem ispum", "20/0902/2",list[ticket_item])    
#jsonStr = json.dumps(user1.__dict__)
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "abcd"  # should be kept secret
JWT_REFRESH_SECRET_KEY = "ohhhtest"    # should be kept secret

def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + delta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    print("TOKEN:", encoded_jwt)
    return encoded_jwt

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#models.Base.metadata.create_all(bind=engine)

#create user 
@app.post("/create_user",response_model = schemas.UserInfoBase)
def create_user(user: schemas.UserInfoBase):
    #crud.create_access_token(user.username)
    #user_obj = schemas.UserInfoBase(user)
    user_obj = json.loads(user.json())

    with open("sample.json", "w") as outfile:
        outfile.write(json.dumps(user_obj))
    return 


#get user info
@app.get("/get_dashboard", response_model=schemas.UserInfoBase,  dependencies=[Depends(jwt_token.JWTBearer())])
def get_user(username, token: str = Depends(oauth2_scheme)):
    #db_user = crud.get_user_by_username(db, username=username)
    with open("sample.json", "r") as file:
        fileData  = file.read()
        jsonData = json.loads(fileData)
    return jsonData

@app.get("/token")
async def read_items(username):
    return {
         "token": create_access_token(username)
    }

''''
#get user's picture
@app.get("/get_profile_picture}", response_model=schemas.UserInfo,  dependencies=[Depends(JWTBearer())])
def get_user(username, db:Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_user = crud.get_user_by_username(db, username=username)
    return db_user

#get user ticket 
@app.get("/get_last_ticket}", response_model=schemas.UserInfo,  dependencies=[Depends(JWTBearer())])
def get_user(username, db:Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_user = crud.get_user_by_username(db, username=username)
    return db_user

#set user info
@app.post("/modify_info", dependencies=[Depends(JWTBearer())])
def add_item( userphone:schemas.UserPayment ,db: Session = Depends(get_db)):
    print('Id: ', userphone.id)
    user_payment = crud.payment(db, phone_number=userphone.phonenumber, id =userphone.id)
    if user_payment:
        return user_payment
       # raise HTTPException(status_code=200, detail=user_payment)
    else:
        raise HTTPException(status_code=400, detail="error")

'''