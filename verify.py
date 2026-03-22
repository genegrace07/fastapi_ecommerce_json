from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException
from dotenv import load_dotenv
from jose import jwt
from jose.exceptions import JWTError,ExpiredSignatureError
import os

load_dotenv()
bearer_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
ALGORITHM=os.getenv('algorithm')
SECRET_KEY=os.getenv('secretkey')

def verify_token(token:str=Depends(bearer_scheme)):
    try:
        token_verified=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return token_verified
    except ExpiredSignatureError:
        raise HTTPException(status_code=401,detail='token expired')
    except JWTError:
        raise HTTPException(status_code=401,detail='invalid token')

