import json
from fastapi import HTTPException

users = 'users.json'
data = 'data.json'
ordered = 'order.json'

users_cached = None
products_cached = None
order_cached = None

def users_cache():
    global users_cached
    if users_cached is None:
        try:
            with open(users,'r') as f:
                users_cached = json.load(f)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="json file not found")
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="json file invalid")
    return users_cached
def products_cache():
    global products_cached
    if products_cached is None:
        try:
            with open(data,'r') as f:
                products_cached = json.load(f)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="json file not found")
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="json file invalid")
    return products_cached

def save_user(update_user):
    global users_cached
    try:
        with open(users, 'w') as f:
            json.dump(update_user,f,indent=4)
            users_cached=update_user
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="json file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="json file invalid")
def save_product(update_product):
    global products_cached
    try:
        with open(data, 'w') as f:
            json.dump(update_product,f,indent=4)
            products_cached=update_product
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="json file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="json file invalid")
def order_cache():
    global order_cached
    try:
        if order_cached is None:
            with open(ordered,'r') as f:
                order_cached = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="json file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="json file invalid")
    return order_cached

