from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# create a resourse that can respond to a GET
class Item(Resource):
    # now the parser belongs to the class and can vbe used in multiple functions
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float, 
        required=True,
        help="This field cannot be left blank!")
    parser.add_argument('store_id',
        type=int, 
        required=True,
        help="Every item needs a store id")
    
    @jwt_required() #so authentication will be required to use this class
    def get(self, name):
            item = ItemModel.find_by_name(name)
            if item:
                return item.json()
            return {'message':'Item not found'},404

   
    def post (self,name):
        if  ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        # this parses the JSON to check the type and only allow price through
        data = Item.parser.parse_args()
        # item= ItemModel(name, data['price'],data['store_id'])
        item= ItemModel(name, **data) # exact equivilent of above!!
        try:
            item.save_to_db()
        except:
            return{"message":"An error occurred inserting the item."}, 500 #internal server error  
        return item.json(), 201 #return code from saved

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'Item deleted'}

        
    def put (self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            # if it is not found create a new one
            item = ItemModel(name, **data)
        else:
            # it is was found change the price
            item.price = data['price']
            item.store_id = data['store_id']
        
        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        # use a list comprehension - reads well
        return {'items': [item.json() for item in ItemModel.query.all()]}
        