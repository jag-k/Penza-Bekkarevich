from . import db_session
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Cart(SqlAlchemyBase):
    __tablename__ = 'cart'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    product = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("guitars.id"), nullable=True)
    quantity = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    cost = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    guitar = orm.relation("Guitars")
    user = orm.relation("User")
