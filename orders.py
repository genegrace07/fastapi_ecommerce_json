from fastapi import HTTPException
import json
from cache import order_cache

orders = 'order.json'
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
    order_cached = order_cache()
    try:
        with open(orders, 'w') as f:
            json.dump(ordered,f,indent=4)
            order_cached = ordered
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="json file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail='json file is invalid')

