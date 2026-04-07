from fastapi import HTTPException
import json
import os

orders = 'order.json'
# def if_blank_order():
#     put_this = []
#     with open(orders,'w') as f:
#         json.dump(put_this,f,indent=4)
def order_list():
    try:
        with open(orders,'r') as f:
            view_orders = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404,detail="json file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500,detail='json file is invalid')
    return view_orders

def save_orders(ordered):
    try:
        with open(orders, 'w') as f:
            json.dump(ordered,f,indent=4)
            # order_cached = ordered
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="json file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail='json file is invalid')
def total_order():
    try:
        if os.path.getsize(orders) == 0:
            return {'message':'no order'}
        with open(orders,'r') as f:
            order_list = json.load(f)
        total = [o['total_price'] for o in order_list]
        grand_total = sum(total)
        return
    except FileNotFoundError:
        raise HTTPException(status_code=404,detail='json file not found')
    except json.JSONDecodeError:
        raise HTTPException(status_code=400,detail='invalid json file')


