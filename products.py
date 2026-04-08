from fastapi import APIRouter,Depends,HTTPException
from verify import verify_token
import json
from cache import products_cache
from orders import order_list,save_orders
from model import Orders as order_request
import os

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
        ordered = order_list()
        if not ordered:
            return {'message':'no orders'}
        # ordered = {o for o in orders_cached if o['user_id'] == payload_token['id']}
        return ordered
@router2.post('/request_order')
async def get_orders(order:order_request,payload_token:dict=Depends(verify_token)):
    if payload_token:
        cached = products_cache()
        ordered = order_list()
        product_id = order.product_id
        quantity = order.quantity
        orders = ordered

        if_match = next((c for c in cached if c['id'] == product_id),None)
        grand_total = 0
        total = quantity * if_match['price']
        grand_total += total

        if len(orders) == 0:

            new_item = {"product_id": if_match['id'], "name": if_match['items'], "price": if_match['price'],
                        "quantity": quantity, "total": total}
            new_order = {"order_id": len(ordered) + 1, "user_id": payload_token['id'], "items": [], "grand_total":grand_total}
            new_order['items'].append(new_item)
            orders.append(new_order)
            save_orders(orders)
            return {'message': 'order added'}

        match_product_id = next((o['product_id'] for o in orders[0]['items'] if product_id == o['product_id'] ),None)
        if not if_match:
            raise HTTPException(status_code=404,detail='product id not found')


        if product_id == match_product_id:
            return {'message': 'item already been added, go to update product'}
        new_item = {"product_id": if_match['id'], "name": if_match['items'], "price": if_match['price'],
                    "quantity": quantity, "total": total}
        grand_total += orders[0]['items'][0]['total']
        orders[0]['items'].append(new_item)
        save_orders(orders)
        return {'message': 'order added'}
    raise HTTPException(status_code=401,detail='invalid token')
@router2.put('/update_order')
async def order_update(order:order_request,payload_token:dict=Depends(verify_token)):
    quantity = order.quantity
    product_id = order.product_id
    if not payload_token:
        raise HTTPException(status_code=401,detail='invalid token')
    ordered_list = order_list()
    order,item = next(((o,i) for o in ordered_list for i in o['items'] if i['product_id'] == product_id), (None,None))
    if not item:
        raise HTTPException(status_code=404,detail='product id not found')
    total = 0
    item['quantity'] = quantity
    sub_total = quantity * item['price']
    item['total'] = sub_total
    total += item['total']
    print(total)
    save_orders(ordered_list)
    return {'message':'successfully updated'}

#TO BE CONTINUE: GRAND TOTAL
