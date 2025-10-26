"""
Import all models here for Alembic to detect them
"""
from app.db.base_class import Base
from app.models.user import User
from app.models.passenger import Passenger
from app.models.station import Station
from app.models.train import Train
from app.models.seat import Seat
from app.models.order import Order, OrderPassenger

