import json
from fastapi import FastAPI,HTTPException,Depends,Form
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from dotenv import load_dotenv
from passlib.hash import sha256_crypt
import os
from model import Products,Users
from datetime import datetime,timedelta
from jose import jwt
from verify import verify_token

app = FastAPI()
data = 'data.json'
users = 'users.json'
load_dotenv()
ALGORITHM = os.getenv('algorithm')
SECRET_KEY = os.getenv('secretkey')
exp = 15
def create_admin():
    user_list = []
    if os.path.exists(users):
        with open(users,'r') as f:
            user_list = json.load(f)
        if_have_default = any(u['username'] == 'admin' for u in user_list)
        if not if_have_default:
            password = os.getenv('admin_password')
            hashed_pwd = sha256_crypt.hash(password)
            admin_login = {'id':1,'username':'admin','password':hashed_pwd}
            user_list.append(admin_login)
            with open(users,'w') as f:
                json.dump(user_list,f,indent=4)
@app.on_event("startup")
def startup_event():
    create_admin()
@app.post('/login',include_in_schema=True)
async def user_login(credentials:OAuth2PasswordRequestForm=Depends()):
    username=credentials.username
    password=credentials.password
    try:
        with open(users,'r') as f:
            users_list=json.load(f)
        if_match=next((u for u in users_list if credentials.username == u['username']),None)
        if if_match:
            verify_pwd=sha256_crypt.verify(credentials.password,if_match['password'])
            if verify_pwd:
                expire_time = datetime.utcnow() + timedelta(minutes=exp)
                for_payload = {'id':if_match['id'],'username':if_match['username'],'exp':expire_time}
                user_token = jwt.encode(for_payload,SECRET_KEY,algorithm=ALGORITHM)
                return {'access_token':user_token,'token_type':'bearer'}
            raise HTTPException(status_code=400,detail="wrong password")
        raise HTTPException(status_code=404,detail="username not found")
    except FileNotFoundError:
        raise HTTPException(status_code=404,detail='json file not found')
    except json.JSONDecodeError:
        raise HTTPException(status_code=404,detail='invalid json file')
@app.get('/')
async def view_products(payload_token:dict=Depends(verify_token)):
    if payload_token:
        try:
            with open(data,'r') as f:
                view_list = json.load(f)
            return view_list
        except FileNotFoundError:
            raise HTTPException(status_code=404,detail="json file not found")
        except json.JSONDecodeError:
            raise HTTPException(status_code=500,detail="json file invalid")
    raise HTTPException(status_code=403,detail="not found, no permission")
@app.post('/signup')
def user_signup(username:str,password:str,payload_token:dict=Depends(verify_token)):
    if payload_token['username'] == 'admin':
        try:
            users_list = []
            with open(users,'r') as f:
                users_list = json.load(f)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="json file not found")
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="json file invalid")

        if_match = next((u for u in users_list if username == u['username']), None)
        if if_match:
            raise HTTPException(status_code=400,detail='username already used')
        hash_pwd = sha256_crypt.hash(password)
        new_user= {'id':len(users_list)+1,'username':username,'password':hash_pwd}
        users_list.append(new_user)
        with open(users,'w') as f:
            json.dump(users_list,f,indent=4)
        raise HTTPException(status_code=201,detail='user created successfully')
    raise HTTPException(status_code=403,detail='No permission')

'''
update github
next delete
'''