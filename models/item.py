from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    #The id is new but good practice to add
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    # link the item table to the store table
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self,name,price,store_id):
        # define what is an item
        self.name = name
        self.price=price
        self.store_id=store_id
    
    def json(self):
        # return a JSON representation of the model in a dictionary
        return {'id':self.id, 'name': self.name,'price': self.price,'store_id': self.store_id}

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first() #select * from items where name=?

    def save_to_db(self): # this replaces both insert and update
        # a sesssion can contain multiple actions
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
