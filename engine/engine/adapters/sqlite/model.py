from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
Base = declarative_base()


class GameState(Base):
    """A given state in a scene. A new state is created when a command is given"""
    __tablename__ = 'game_state'

    id = Column(Integer, primary_key=True, index=True)
    x_coordinate = Column(Integer)
    y_coordinate = Column(Integer)
    health_points = Column(Integer)
    scene = Column(String)
    created = Column(DateTime)

    game_id = Column(
        Integer, ForeignKey("game.id"),
    )
#     # todo- inventory
#     # todo- fk on Game


class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True, index=True)
    game_states = relationship("GameState", order_by=GameState.created, backref="game")
    # name
    # coordinates explored ?
    # inventory collected ?


