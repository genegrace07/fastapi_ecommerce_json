from fastapi import APIRouter,Depends,HTTPException
from verify import verify_token
import json
from cache import products_cache,order_cache
from orders import order_list,save_orders
from model import Orders as order_request

router = APIRouter(prefix='/products',tags=['Products'])
router2 = APIRouter(prefix='/orders',tags=['orders'])
data = 'data.json'

@router.get('/')
async def view_products(payload_token:dict=Depends(verify_token)):
    cached = products_cache()
    if payload_token:
        return cached
    raise HTTPException(status_code=403,detail="not found, no permission")
@router2.get('/view_order')
async def view_orders(payload_token:dict=Depends(verify_token)):
    if payload_token:
        orders_cached = order_cache()
        if not orders_cached:
            return {'message':'no orders'}
        ordered = {o for o in orders_cached if o['user_id'] == payload_token['id']}
        return ordered
@router2.post('/request_order')
async def get_orders(order:order_request,payload_token:dict=Depends(verify_token)):
    if payload_token:
        cached = products_cache()
        cache_order = order_cache()
        order_id = order.product_id
        quantity = order.quantity
        if_checkout = order.if_checkout
        if_match = next((c for c in cached if c['id'] == order_id),None)
        existing_order = [c for c in cache_order]
        total = quantity * if_match['price']
        new_order = {"order_id":len(existing_order)+1,"user_id":payload_token['id'],"items":[
        {
            "product_id": if_match['id'],
            "name": if_match['items'],
            "price": if_match['price'],
            "quantity": quantity
        }],"total_price":total}
        if if_checkout == 'yes':
            save_orders(cache_order)
            cache_order.clear()
            return {'message': 'order completed'}
        cache_order.append(new_order)
        # print(cache_order)
        return {'message': 'order added'}
    raise HTTPException(status_code=401,detail='invalid token')
