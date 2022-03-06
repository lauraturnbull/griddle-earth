from typing import Any

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship


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


metadata = MetaData()
Base = make_declarative_base()  # type: Any


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    item_type = Column(String, nullable=False)
    health_points = Column(Integer, nullable=False)
    collection_method = Column(String, nullable=False)
    adventure_log_discovered_items = Column(
        Integer, ForeignKey("adventure_log.id")
    )
    adventure_log_discoverable_items = Column(
        Integer, ForeignKey("adventure_log.id")
    )
    items_id = Column(Integer, ForeignKey("items.id"))


class Items(Base):
    """An inventory of items"""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    item = relationship("Item", backref="items", uselist=False)

    component_id = Column(Integer, ForeignKey("component.id"))
    inventory_id = Column(Integer, ForeignKey("inventory.id"))


class Component(Base):
    __tablename__ = "component"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_gateway = Column(Boolean, nullable=False)
    transports_to_x_coordinate = Column(Integer, nullable=True)
    transports_to_y_coordinate = Column(Integer, nullable=True)
    items = relationship("Items", backref="component", cascade="all")

    location_id = Column(Integer, ForeignKey("location.id"))


class Location(Base):
    """The state of a location on the map"""

    __tablename__ = "location"

    id = Column(Integer, primary_key=True, index=True)
    x_coordinate = Column(Integer, nullable=False)
    y_coordinate = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    region = Column(String, nullable=False)
    components = relationship("Component", backref="location", cascade="all")

    game = relationship("Game", back_populates="location")
    game_id = Column(Integer, ForeignKey("game.id"))
    map_id = Column(Integer, ForeignKey("map.id"))

    adventure_log_discovered_locations = Column(
        Integer, ForeignKey("adventure_log.id")
    )
    adventure_log_discoverable_locations = Column(
        Integer, ForeignKey("adventure_log.id")
    )


class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    items = relationship("Items", backref="inventory", cascade="all")

    game = relationship("Game", back_populates="inventory")
    game_id = Column(Integer, ForeignKey("game.id"))


class Game(Base):
    """
    The state of the entire game: player, inventory and location
    The equivalent of "saves".
    """

    __tablename__ = "game"

    id = Column(Integer, primary_key=True, index=True)
    health_points = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False)

    location = relationship(
        "Location", back_populates="game", uselist=False, cascade="all"
    )
    inventory = relationship(
        "Inventory", back_populates="game", uselist=False, cascade="all"
    )


class Map(Base):
    __tablename__ = "map"

    id = Column(Integer, primary_key=True, index=True)
    locations = relationship("Location", backref="map", cascade="all")
    game_id = Column(Integer, ForeignKey("game.id"))
    game = relationship("Game", backref=backref("map", uselist=False))


class AdventureLog(Base):
    __tablename__ = "adventure_log"

    id = Column(Integer, primary_key=True, index=True)

    discovered_locations = relationship(
        "Location",
        foreign_keys=Location.adventure_log_discovered_locations,
        cascade="all",
    )
    discoverable_locations = relationship(
        "Location",
        foreign_keys=Location.adventure_log_discoverable_locations,
        cascade="all",
    )
    discovered_items = relationship(
        "Item", foreign_keys=Item.adventure_log_discovered_items, cascade="all"
    )
    discoverable_items = relationship(
        "Item",
        foreign_keys=Item.adventure_log_discoverable_items,
        cascade="all",
    )

    game_id = Column(Integer, ForeignKey("game.id"))
    game = relationship(
        "Game", backref=backref("adventure_log", uselist=False)
    )
