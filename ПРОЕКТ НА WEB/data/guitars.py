from . import db_session
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Guitars(SqlAlchemyBase):
    __tablename__ = 'guitars'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cart = orm.relation("Cart", back_populates="guitar")
