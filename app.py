from fastapi import FastAPI
from users import create_admin,router as users_router
from products import router as products_router

app = FastAPI()
app.include_router(users_router)
app.include_router(products_router)

@app.on_event("startup")
def startup_event():
    create_admin()

'''
#read user list admin access
#Admin can change users: username,password reset,role
#Admin only can delete users
#use max() for id
#hide hash password

admin access for create,read,update,delete product
normal user can create,read,update,delete order
-ADJUSTMENT-
organize modules
create cache for json
separate admin endpoint for signup
'''