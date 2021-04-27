from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # link back to other table which has a foreign key to here
    items = db.relationship('ItemModel', lazy='dynamic') #this is a list of ItemModels (that are in the store)
    # lazy='dynamic' doesn't create all possible cross links when you have a new store (don't really understand)

    def __init__(self,name):
        # define what is an item
        self.name = name
            
    def json(self):
        # return a JSON representation of the model in a dictionary (note more than one items in a list)
        return {'id':self.id, 'name': self.name,'items': [item.json() for item in self.items.all()]}

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
