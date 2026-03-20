from fastapi import APIRouter,Depends,HTTPException
from verify import verify_token
import json
from cache import products_cache

router = APIRouter(prefix='/products',tags=['Products'])
data = 'data.json'

@router.get('/')
async def view_products(payload_token:dict=Depends(verify_token)):
    cached = products_cache()
    if payload_token:
        return cached
    raise HTTPException(status_code=403,detail="not found, no permission")