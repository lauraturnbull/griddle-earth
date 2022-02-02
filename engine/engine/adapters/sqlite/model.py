from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
Base = declarative_base()


# todo - inventory
# class Inventory(Base):
#     ingredients = []  # fruit, veg, meat, fish, herbs, grains? +- hp
#     dishes = []
#     tools = []  # flint, knife, wood?


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    item_type = Column(String)
    health_points = Column(Integer)


class Items(Base):
    """An inventory of items"""
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship("Item", uselist=False)

    location_id = Column(Integer, ForeignKey('location.id'))
    inventory_id = Column(Integer, ForeignKey('inventory.id'))


class Location(Base):
    """The state of a location on the map"""
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    x_coordinate = Column(Integer)
    y_coordinate = Column(Integer)
    name = Column(String)
    description = Column(String)
    region = Column(String)
    items = relationship("Items", order_by=Items.id, backref="location")

    game = relationship("Game", back_populates="location")
    game_id = Column(Integer, ForeignKey('game.id'))


class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True)
    items = relationship("Items", backref="inventory")

    game = relationship("Game", back_populates="inventory")
    game_id = Column(Integer, ForeignKey('game.id'))


class Game(Base):
    """
    The state of the entire game: player, inventory and location
    The equivalent of "saves".
    """
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True, index=True)
    health_points = Column(Integer)
    created = Column(DateTime)

    location = relationship("Location", back_populates="game", uselist=False)
    inventory = relationship("Inventory", back_populates="game", uselist=False)



