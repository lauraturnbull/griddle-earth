from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref


def make_declarative_base():
    Base = declarative_base()

    Base.metadata.naming_convention = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    return Base


Base = make_declarative_base()

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
    adventure_log_discovered_items = Column(Integer, ForeignKey('adventure_log.id'))
    adventure_log_discoverable_items = Column(Integer, ForeignKey('adventure_log.id'))


class Items(Base):
    """An inventory of items"""
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship("Item", uselist=False)

    component_id = Column(Integer, ForeignKey('component.id'))
    inventory_id = Column(Integer, ForeignKey('inventory.id'))


class Component(Base):
    __tablename__ = "component"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    items = relationship("Items", backref="component")

    location_id = Column(Integer, ForeignKey('location.id'))


class Location(Base):
    """The state of a location on the map"""
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True, index=True)
    x_coordinate = Column(Integer)
    y_coordinate = Column(Integer)
    name = Column(String)
    description = Column(String)
    region = Column(String)
    components = relationship("Component", backref="location")

    game = relationship("Game", back_populates="location")
    game_id = Column(Integer, ForeignKey('game.id'))
    map_id = Column(Integer, ForeignKey('map.id'))

    adventure_log_discovered_locations = Column(Integer, ForeignKey('adventure_log.id'))
    adventure_log_discoverable_locations = Column(Integer, ForeignKey('adventure_log.id'))


class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
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


class Map(Base):
    __tablename__ = "map"

    id = Column(Integer, primary_key=True, index=True)
    locations = relationship("Location", backref="map")
    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship("Game", backref=backref("map", uselist=False))


class AdventureLog(Base):
    __tablename__ = "adventure_log"

    id = Column(Integer, primary_key=True, index=True)

    discovered_locations = relationship("Location", foreign_keys=Location.adventure_log_discovered_locations)
    discoverable_locations = relationship("Location", foreign_keys=Location.adventure_log_discoverable_locations)
    discovered_items = relationship("Item", foreign_keys=Item.adventure_log_discovered_items)
    discoverable_items = relationship("Item", foreign_keys=Item.adventure_log_discoverable_items)

    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship("Game", backref=backref("adventure_log", uselist=False))