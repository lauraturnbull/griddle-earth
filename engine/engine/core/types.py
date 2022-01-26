from pydantic import BaseModel


class Command(BaseModel):
    action: str
    context: str


class Coordinates(BaseModel):
    x: int = 0
    y: int = 0


class GameState(BaseModel):
    coordinates: Coordinates = Coordinates()
    health_points: int = 1000
    scene: str
    # created_at = Column(DateTime)