from fastapi import APIRouter,Depends,HTTPException
from verify import verify_token
import json
from cache import products_cache
from orders import order_list,save_orders,total_order
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
        grand_total = total_order()

        if not if_match:
            raise HTTPException(status_code=404,detail='product id not found')

        if len(orders) == 0:
            total = quantity * if_match['price']
            new_item = {"product_id": if_match['id'], "name": if_match['items'], "price": if_match['price'],
                        "quantity": quantity, "total": total}
            new_order = {"order_id": len(ordered) + 1, "user_id": payload_token['id'], "items": [],"grand_total":total}
            new_order['items'].append(new_item)
            orders.append(new_order)
            print(grand_total)
            save_orders(orders)
            return {'message': 'order added'}

        match_product_id = next((o['product_id'] for o in orders[0]['items'] if product_id == o['product_id'] ),None)

        if product_id == match_product_id:
            return {'message': 'item already been added, go to update product'}
        total = quantity * if_match['price']
        new_item = {"product_id": if_match['id'], "name": if_match['items'], "price": if_match['price'],
                    "quantity": quantity, "total": total}
        final_total = grand_total + total
        orders[0]['grand_total'] = final_total
        orders[0]['items'].append(new_item)
        save_orders(orders)
        return {'message': 'order added'}
    raise HTTPException(status_code=401,detail='invalid token')
@router2.put('/update_order')
async def order_update(order:order_request,payload_token:dict=Depends(verify_token)):
    quantity = order.quantity
    product_id = order.product_id
    cached = products_cache()
    grand_total = total_order()

    if not payload_token:
        raise HTTPException(status_code=401,detail='invalid token')
    ordered_list = order_list()
    order1,item = next(((o,i) for o in ordered_list for i in o['items'] if i['product_id'] == product_id), (None,None))
    if not item:
        raise HTTPException(status_code=404,detail='product id not found')
    new_total = item['price'] * quantity
    item['quantity'] = quantity
    item['total'] = new_total
    get_total = [o['total'] for o in order1['items']]
    order1['grand_total'] = sum(get_total)
    # print(sum(get_total))
    save_orders(ordered_list)
    return {'message':'successfully updated'}
@router2.delete('/delete_order/{product_id}')
async def order_delete(product_id:int,payload_token:dict=Depends(verify_token)):
    if not payload_token:
        raise HTTPException(status_code=401,detail='invalid token')
    ordered = order_list()
    if_match_order = next((o for o in ordered if o['user_id'] == payload_token['id']),None)
    if_match_item = next((i for i in if_match_order['items'] if product_id == i['product_id']),None)
    if not if_match_order:
        raise HTTPException(status_code=404,detail='user id not found')
    if not if_match_item:
        raise HTTPException(status_code=404,detail='product id not found')
    new_grand_total = if_match_order['grand_total'] - if_match_item['total']
    if_match_order['grand_total'] = new_grand_total
    if_match_order['items'].remove(if_match_item)
    save_orders(ordered)
    return {'message':'order deleted'}

#TO BE CONTINUE: AFTER ORDER DELETED,UPDATE GRAND TOTAL, QUANTITY CANNOT BE 0, CANNOT BE EXCEED TO CURRENTLY QUANTITY








