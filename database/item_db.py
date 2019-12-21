from sqlalchemy_db import db


class ItemModel(db.Model):

    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")


    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id


    def toDict(self):
        return {
            "name": self.name,
            "price": self.price,
            "store_id": self.store_id
        }


    @classmethod
    def all_items(cls):
        try:
            return {"items": [item.toDict() for item in ItemModel.query.all()]}
        except Exception as e:
            raise Exception(e)


    @classmethod
    def find_item(cls, name):
        try:
            return ItemModel.query.filter_by(name=name).first()
        except Exception as e:
            raise Exception(e)


    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.find_item(self.name)
        except Exception as e:
            raise Exception(e)


    def delete_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            raise Exception(e)
