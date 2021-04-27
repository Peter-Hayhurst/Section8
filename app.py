from flask import Flask
from flask_restful import Api
# pick up the JWT security library and the decorator (jwt_required)
from flask_jwt import JWT
# and our routines from the security.py file
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
 
app = Flask(__name__)
#sqlalchemy can work with MSSQL / MySQL / Oracle etc, but in this case sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose' #idealy long and complicated
api = Api(app)



# this tells JWT about the key and the functions used in security
jwt=JWT(app, authenticate, identity) # creates a new end point /auth

api.add_resource(Store,'/store/<string:name>') 
api.add_resource(Item,'/item/<string:name>') 
api.add_resource(ItemList,'/items') 
api.add_resource(StoreList,'/stores') 
api.add_resource(UserRegister,'/register') 

# test code
#print("Hello world")
#print(app.secret_key)
#usr=User.find_by_username('jose')
#print(usr)

# only run the app when running this code (not just importing)
if __name__ == '__main__':
    # import now to avoid circular import
    from db import db
    db.init_app(app) # app is the flask app
    app.run(port=5000, debug=True)