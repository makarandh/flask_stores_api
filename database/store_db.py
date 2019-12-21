from sqlalchemy_db import db


class StoreModel(db.Model):

    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    items = db.relationship("ItemModel", lazy="dynamic")
    # when we put lazy=dynamic, the objects are not immediately created
    # so there is initial time saving. But every time we query an item
    # it becomes slow.
    # So either we can have slow start, or slow queries


    def __init__(self, name):
        self.name = name


    def toDict(self):
        return {
            "name": self.name,
            "items": [item.toDict() for item in self.items.all()]
        }


    @classmethod
    def all_items(cls):
        try:
            return {"stores": [item.toDict() for item in StoreModel.query.all()]}
        except Exception as e:
            raise Exception(e)


    @classmethod
    def find_by_name(cls, name):
        try:
            return StoreModel.query.filter_by(name=name).first()
        except Exception as e:
            raise Exception(e)


    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.find_by_name(self.name)
        except Exception as e:
            raise Exception(e)


    def delete_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            raise Exception(e)
