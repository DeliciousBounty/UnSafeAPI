from typing import List, Union
from xmlrpc.client import DateTime
from pydantic import BaseModel,Field, validator
from sqlalchemy import Column, Integer, String
import uuid
from datetime import datetime

class UserInfo:
    def __init__ (self, username, fullname,address, email, date_of_brith, ticket_list ):
        self.username =username
        self.fullname = fullname
        self.address  = address
        self.email = email
        self.date_of_brith = date_of_brith
        self.ticket_list = ticket_list



class Ticket:
	def __init__(self, uuid, date, text, title, level):
		self.uuid = uuid
		self.date = date
		self.text = text
		self.title = title
		self.level = level

#base schema for tickets
class TicketInfo(BaseModel):
    uuid:str = Field(..., description= "name of the item", min_length=3,max_length=36, example= uuid.uuid4()) 
    date:datetime = Field(..., description= "creation date", example= datetime.utcnow())
    title:str = Field(..., description  ="Title of the ticket", min_length=5, max_length=15)
    text:str = Field(..., description  ="Message  inside  the ticket", min_length=5, max_length=50)
    level:int = Field(..., description  ="Title of the ticket", min = 1, max = 6, example = 3)

    @validator("level")
    @classmethod
    def check_valid_level(cls,value):
        if value > 5:
            raise ValueError("Level value cannot be above 5.")
        return value

    class Config:
        orm_mode = True

# base schema for user data
class UserInfoBase(BaseModel):
    username:str = Field(...,description= "username of the website", min_length=3,max_length=15, example= "user_test")
    fullname:str = Field(..., description= "username and last name", max_length=20, example= "John Doe")
    address:str= Field(...,description = "address of the user")
    email:str = Field(...,description = "user's email")
    date_of_brith:str = Field(..., description  = " date of brith")
    max_open_ticket:int = Field(..., description="The maximmum ticket per user",max=5)
    ticket_list: list[TicketInfo] = Field(..., description="add Ticket")
        
class Token(BaseModel):
    token:str

 


