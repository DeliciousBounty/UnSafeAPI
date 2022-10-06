from datetime import datetime
from datetime import timedelta as delta
from optparse import TitledHelpFormatter
from sqlite3 import Date
from tokenize import String
from uuid import UUID
import os
from typing import Any, List, Union
from fastapi.openapi.models import Server
from urllib import request, response
import uvicorn
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException,Body, status, Query, Security
from fastapi.security import OAuth2PasswordBearer #security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse
import json
from typing import List, Union
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
    try:
        filename ="./users/"+subject+".json" 
        with open(filename, "r") as file:
            fileData  = file.read()
            jsonData = json.loads(fileData)
            user_type = jsonData["user_type"]
    except:
        user_type = "user" 
    to_encode = {"exp": expires_delta, "sub": str(subject), "user_type": str(user_type)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    
    print("Token encoded", encoded_jwt)
    verify_jwt(encoded_jwt)
    return encoded_jwt

def verify_jwt(jwtoken: str) -> str:
        isTokenValid: bool = False
        try:
            payload = jwt.decode(jwtoken, JWT_SECRET_KEY, algorithms=[ALGORITHM])
            # print(payload)
            return payload["sub"],payload["user_type"]
        except Exception as e:
            print("Errorr", e)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
        )

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#create user 
@app.post("/create_user",response_model = schemas.UserInfoBase)
def create_user(user: schemas.UserInfoBase):
    username =user.username
    json_file = username+".json"
    user_obj = json.loads(user.json())
    with open("./users/"+json_file, "w") as outfile:
        outfile.write(json.dumps(user_obj))
    return 


#get user info
@app.get("/get_dashboard", response_model=schemas.UserInfoBase,  dependencies=[Depends(jwt_token.JWTBearer())])
def get_user(username, token: str = Depends(jwt_token.JWTBearer())):
    user, user_type = verify_jwt(token)
    if user and user !="":
        try:
            with open(user+".json", "r") as file:
                fileData  = file.read()
                jsonData = json.loads(fileData)
            return jsonData
        except:
            raise HTTPException(status_code=404, detail="Error maybe user not exists or corrupt file")

@app.get("/token")
async def create_token(username):
    return {
         "token": create_access_token(username)
    }


#get all users only for admin
@app.get("/get_users",  dependencies=[Depends(jwt_token.JWTBearer())])
def get_all_users(token: str = Depends(jwt_token.JWTBearer())):
    user, user_type  = verify_jwt(token)
    json_data= []
    if user_type == "admin": # only if is admin
        for i in os.listdir('./users'):
            with open("./users/"+i, "r") as file:
                fileData  = file.read()
                jsonData = json.loads(fileData)
                json_data.append(jsonData)

    return json_data

@app.get("/token")
async def create_token(username):
    return {
         "token": create_access_token(username)
    }


#get user ticket 
@app.get("/get_last_ticket", response_model=schemas.TicketInfo,  dependencies=[Depends(jwt_token.JWTBearer())])
def get_user(token: str = Depends(jwt_token.JWTBearer())):
     user, user_type  = verify_jwt(token)
     if user in [i.split(".")[0] for i in os.listdir('./users')]:
        with open("./users/"+user+".json", "r") as file:
            fileData = file.read()
            jsonData = json.loads(fileData)
            print(jsonData["ticket_list"])
        return jsonData["ticket_list"][len(jsonData["ticket_list"])-1]
     else:
        raise HTTPException(status_code=400, detail = "user not exisiting")


#remove ticket
@app.delete("/ticket",dependencies=[Depends(jwt_token.JWTBearer())] , include_in_schema=False)
def ticket_removing(token: str = Depends(jwt_token.JWTBearer())):
    user, user_type  = verify_jwt(token)
    if user in [i.split(".")[0] for i in os.listdir('./users')]:
        os.remove("./users/"+user+".json")
        return {"message": "remove successfully"}
    else:
        raise HTTPException(status_code=404, detail= "forbidden")


#add ticket to user
@app.post("/ticket")
def ticket_adding(ticket: schemas.TicketInfo, token: str = Depends(jwt_token.JWTBearer())):
    user_obj = json.loads(ticket.json())
    user, user_type  = verify_jwt(token)
    if user in [i.split(".")[0] for i in os.listdir('./users')]:
        with open("./users/"+user+".json", "r") as outfile:
            fileData = outfile.read()
            jsonData = json.loads(fileData)
            print(jsonData["ticket_list"])
            max = jsonData["max_open_ticket"]
            if len(jsonData["ticket_list"])> max:
                jsonData["ticket_list"].append(user_obj)
                with open("./users/"+user+".json", "w") as json_file:
                    json.dump(jsonData,json_file)
                return {"message":"success"}
            else:
                return {"message":"too much tickets for this user"}
    else:
        raise HTTPException(status_code=400, detail = "user not exisiting")

@app.get("/back_home/")
async def redirect(url: str):
     if (url != None):
        # if(re.search(p, str)):
        response = RedirectResponse(url,status_code=303)
        return response
     else:
        return False
#@app.get("get_all_users")
