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
        with open(orders,'r') as f:
            order_list = json.load(f)
        if not order_list:
            return 0
        total = [o['total'] for o in order_list[0]['items']]
        if not total:
            return 0
        grand_total = sum(total)
        return grand_total

    except FileNotFoundError:
        raise HTTPException(status_code=404,detail='json file not found')
    except json.JSONDecodeError:
        raise HTTPException(status_code=400,detail='invalid json file')


