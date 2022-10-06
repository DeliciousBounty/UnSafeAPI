from copy import deepcopy
from pyexpat import model
from typing import Any, List, Union
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


 #validator for level
# @validator("level")
# @classmethod # Optional, but your linter may like it.
# def check_level(cls, value):
#         if value < 0 or value >= 13:
#             raise ValueError("Level too high or too low")
#         return value

#  #validator for text


#base schema for tickets
class TicketInfo(BaseModel):
    validation= False
    uuid:str = Field(..., description = "name of the item", min_length=3,max_length=36, example= uuid.uuid4()) 
    date:datetime= Field(..., description = "creation date", example= datetime.utcnow())
    title:str = Field(..., description = "Title of the ticket", min_length=5, max_length=15)
    validation = False
    text:str = Field(..., description = "Message  inside  the ticket", min_length=5, max_length=50, validator=False)
    level:int = Field(..., description = "Title of the ticket", min= 2, max=10, example = 1)
    
    # @classmethod
    # def unvalidated(__pydantic_cls__: "Type[Model]", **data: Any) -> TicketInfo:
    #     for name, field in __pydantic_cls__.__fields__.items():
    #         try:
    #             data[name]
    #         except KeyError:
    #             if field.required:
    #                 raise TypeError(f"Missing required keyword argument {name!r}")
    #             if field.default is None:
    #                 # deepcopy is quite slow on None
    #                 value = None
    #             else:
    #                 value = deepcopy(field.default)
    #             data[name] = value
    #     self = __pydantic_cls__.__new__(__pydantic_cls__)
    #     object.__setattr__(self, "__dict__", data)
    #     object.__setattr__(self, "__fields_set__", set(data.keys()))
    #     return self
    # @validator("text",pre=True, always= False)
    # @classmethod # Optional, but your linter may like it.
    # def check_text_length(cls, value):
    #         if len(value) < 2 or len(value) > 20 :
    #             raise ValueError("too much text")
    #         return value


    # class Config:
    #     orm_mode = True

class Config:
    validation= False

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

 


