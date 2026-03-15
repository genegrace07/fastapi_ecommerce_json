from fastapi import APIRouter,Depends,HTTPException
from verify import verify_token
import json

router = APIRouter(prefix='/products',tags=['Products'])
data = 'data.json'
@router.get('/')
async def view_products(payload_token:dict=Depends(verify_token)):
    if payload_token:
        try:
            with open(data,'r') as f:
                users_list = json.load(f)
            return users_list
        except FileNotFoundError:
            raise HTTPException(status_code=404,detail="json file not found")
        except json.JSONDecodeError:
            raise HTTPException(status_code=500,detail="json file invalid")
    raise HTTPException(status_code=403,detail="not found, no permission")