import os

from sqlalchemy import create_engine, Column, Text, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def new_db(path):
    engine = create_engine(path)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine


def new_session(path):
    engine = create_engine(path)
    return sessionmaker(bind=engine)()


def insert_static_data(db):
    for d in ['Breakfast', 'Brunch', 'Lunch', 'Tea', 'Snack', 'Supper', 'Desert']:
        db.add(Label(Descriptor=d))
    db.commit()


class Label(Base):
    __tablename__ = 'Label'
    LabelID = Column(Integer, primary_key=True)
    Descriptor = Column(Text)  # Breakfast, Lunch, Tea, Snack, Brunch, Supper, Desert

    def __str__(self):
        return '<Label[LabelID=%s, Descriptor=%s]>' % (self.LabelID, self.Descriptor)


class Ingredient(Base):
    __tablename__ = 'Ingredient'
    IngredientID = Column(Integer, primary_key=True)
    Descriptor = Column(Text)

    def __str__(self):
        return '<Ingredient[IngredientID=%s, Descriptor=%s]>' % (self.IngredientID, self.Descriptor)


class IngredientQuantityRecepie(Base):
    __tablename__ = 'IngredientQuantityRecepie'
    IngredientQuantityRecepieID = Column(Integer, primary_key=True)
    RecepieID = Column(Integer, ForeignKey('Recepie.RecepieID'))
    IngredientID = Column(Integer, ForeignKey('Ingredient.IngredientID'))
    Quantity = Column(Integer)

    def __str__(self):
        return '<IngredientQuantityRecepie[IngredientQuantityRecepieID=%s, RecepieID=%s, IngredientID=%s, Quantity=%s]>' % (self.IngredientQuantityRecepieID, self.RecepieID, self.IngredientID, self.Quantity)


class Recepie(Base):
    __tablename__ = 'Recepie'
    RecepieID = Column(Integer, primary_key=True)
    Descriptor = Column(Text)
    Serves = Column(Integer)
    LabelID = Column(Integer, ForeignKey(Label.LabelID))
    ingredients = relationship(IngredientQuantityRecepie, primaryjoin='Recepie.RecepieID == IngredientQuantityRecepie.RecepieID')


if __name__ == '__main__':
    DB_FILE_PATH = 'live.db'
    DB_PATH = 'sqlite:///' + DB_FILE_PATH
    new_db(DB_PATH)
    db = new_session(DB_PATH)
    insert_static_data(db)

    print [str(l) for l in db.query(Label).all()]
    db.close()
    os.remove(DB_FILE_PATH)
