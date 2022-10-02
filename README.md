# UnSafeAPI
A Simple RestAPI, Vulnerable by design fast to deploy and easy to use.
This  API simulate a ticket management system and works with JSON files, instead database.

## Code Simples
There are three main files:
### main.py

The main page of the application including all the routes,..
'''
@app.post("/create_user",response_model = schemas.UserInfoBase)
def create_user(user: schemas.UserInfoBase):
    username =user.username
    json_file = username+".json"
    user_obj = json.loads(user.json())
    with open("./users/"+json_file, "w") as outfile:
        outfile.write(json.dumps(user_obj))
    return 
'''
  
### schemas.py
 
Schemas store all class objects
 
 '''
class UserInfoBase(BaseModel):
    username:str = Field(...,description= "username of the website", min_length=3,max_length=15, example= "user_test")
    fullname:str = Field(..., description= "username and last name", max_length=20, example= "John Doe")
    address:str= Field(...,description = "address of the user")
    email:str = Field(...,description = "user's email")
    date_of_brith:str = Field(..., description  = " date of brith")
    max_open_ticket:int = Field(..., description="The maximmum ticket per user",max=5)
    ticket_list: list[TicketInfo] = Field(..., description="add Ticket")
'''
    
### jwt_token.py
    
A simple file describing the JWT Token class.
    
    
    
   
## How to start?
```   
git clone https://github.com/DeliciousBounty/UnSafeAPI.git
pip3 install -r requirements.txt
 uvicorn main:app --reload
```

Then you need to ensure to create a minimum one user with the following endpoint
   ![image](https://user-images.githubusercontent.com/46570579/193453146-75f9d780-1a0c-421e-bae5-250c2ddb7bd6.png)

