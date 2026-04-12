from fastapi import FastAPI
from users import create_admin,user_router as users_router,admin_router as admins_router,auth_router as router_auth
from products import router as products_router,router2 as order_router

app = FastAPI()
app.include_router(users_router)
app.include_router(admins_router)
app.include_router(router_auth)
app.include_router(products_router)
app.include_router(order_router)
@app.on_event("startup")
def startup_event():
    create_admin()


'''
#read user list admin access
#Admin can change users: username,password reset,role
#Admin only can delete users
#use max() for id
#hide hash password
#organize modules
#separate admin endpoint for signup
#create cache for json

normal user can #create,#read,#update,#delete order
admin access for create,read,update,delete product

'''
