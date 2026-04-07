from pydantic import BaseModel

class Products(BaseModel):
    id:int
    sales:str
    items:str
    price:int
    quantity:int
class Users(BaseModel):
    user_id:int
    username:str
    password:str
class Orders(BaseModel):
    # order_id:int
    product_id:int
    quantity:int
    # product_id:int



