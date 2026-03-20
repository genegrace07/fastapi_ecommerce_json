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
from fastapi import APIRouter
from cache import users_cache,save_user

user_router = APIRouter(prefix='/users',tags=['Users'])
admin_router = APIRouter(prefix='/admin',tags=['Admin'])
auth_router = APIRouter(prefix='/auth',tags=['Auth'])
data = 'data.json'
users = 'users.json'
load_dotenv()
ALGORITHM = os.getenv('algorithm')
SECRET_KEY = os.getenv('secretkey')
exp = 15
def create_admin():
    user_cached = users_cache()
    if_have_default = any(u['username'] == 'admin' for u in user_cached)
    if not if_have_default:
        password = os.getenv('admin_password')
        hashed_pwd = sha256_crypt.hash(password)
        admin_login = {'id':1,'username':'admin','password':hashed_pwd,'role':'admin'}
        user_cached.append(admin_login)
        save_user(user_cached)
@auth_router.post('/login',include_in_schema=True)
async def user_login(credentials:OAuth2PasswordRequestForm=Depends()):
    user_cached = users_cache()
    username=credentials.username
    password=credentials.password
    if_match=next((u for u in user_cached if credentials.username == u['username']),None)
    if if_match:
        verify_pwd=sha256_crypt.verify(credentials.password,if_match['password'])
        if verify_pwd:
            expire_time = datetime.utcnow() + timedelta(minutes=exp)
            for_payload = {'id':if_match['id'],'username':if_match['username'],'role':if_match['role'],'exp':expire_time}
            user_token = jwt.encode(for_payload,SECRET_KEY,algorithm=ALGORITHM)
            return {'access_token':user_token,'token_type':'bearer'}
        raise HTTPException(status_code=400,detail="wrong password")
    raise HTTPException(status_code=404,detail="username not found")

@admin_router.post('/signup')
async def user_signup(username:str=Form(...),password:str=Form(...),role:str=Form(...),payload_token:dict=Depends(verify_token)):
    user_cached = users_cache()
    if payload_token['role'] == 'admin':
        if_match = next((u for u in user_cached if username == u['username']), None)
        if if_match:
            raise HTTPException(status_code=400,detail='username already used')
        hash_pwd = sha256_crypt.hash(password)
        if role in ['admin','user']:
            new_id = max(u['id'] for u in user_cached)+1 if user_cached else 1
            new_user= {'id':new_id,'username':username,'password':hash_pwd,'role':role}
            user_cached.append(new_user)
            save_user(user_cached)
            return {'message':'user created successfully'}
        raise HTTPException(status_code=400,detail='role invalid')
    raise HTTPException(status_code=403,detail='No permission')
@admin_router.get('/view_users_list')
async def users_view(payload_token:dict=Depends(verify_token)):
    user_cached = users_cache()
    if payload_token['role'] == 'admin':
        view_list = [{'id':u['id'],'username':u['username'],'role':u['role']} for u in user_cached]
        return view_list
    raise HTTPException(status_code=403,detail='no permission')
@admin_router.put('/update_user')
async def update_user(payload_token:dict=Depends(verify_token),id:int=Form(...),username:str=Form(...),pwd:str=Form(...),role:str=Form(...)):
    user_cached = users_cache()
    if payload_token['role'] == 'admin':
        if_match = next((u for u in user_cached if u['id'] == id),None)
        if if_match:
            if_match['username']=username
            hash_pwd = sha256_crypt.hash(pwd)
            if_match['password']=hash_pwd
            roles = ['admin','user']
            if role not in roles:
                raise HTTPException(status_code=400,detail='not valid role')
            if_match['role'] = role
            save_user(user_cached)
            return {'message':'successfully update'}
        raise HTTPException(status_code=404,detail='not found')
    raise HTTPException(status_code=403,detail='no permission')
@admin_router.delete('/delete_user/{id}')
async def user_delete(id:int,payload_token:dict=Depends(verify_token)):
    user_cached = users_cache()
    if payload_token['role'] == 'admin':
        if_match = next((u for u in user_cached if u['id'] == id),None)
        if if_match:
            if if_match['role'] == 'admin':
                raise HTTPException(status_code=400,detail='cannot delete admin account, change to "user" role first')
            user_cached.remove(if_match)
            save_user(user_cached)
            return {'message':'user successfully deleted'}
        raise HTTPException(status_code=404,detail='not found')
    raise HTTPException(status_code=403,detail='no permission')

