from fastapi import HTTPException
import json

orders = 'order.json'

def order_list():
    try:
        with open(orders,'r') as f:
            view = json.load(f)
        return view
    except FileNotFoundError:
        raise HTTPException(status_code=404,detail="json file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500,detail='json file is invalid')

def save_orders(ordered):
    try:
        with open(orders, 'w') as f:
            view = json.dump(ordered,f,indent=4)
        return view
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="json file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail='json file is invalid')

