import sqlalchemy
from .db_session import SqlAlchemyBase

# outgoing_requests_table = sqlalchemy.Table('outgoing_requests', SqlAlchemyBase.metadata,
#     sqlalchemy.Column('user', sqlalchemy.Integer,
#                       sqlalchemy.ForeignKey('users.id')),
#     sqlalchemy.Column('request', sqlalchemy.Integer,
#                       sqlalchemy.ForeignKey('requests.id'))
# )
# ingoing_requests_table = sqlalchemy.Table('ingoing_requests', SqlAlchemyBase.metadata,
#     sqlalchemy.Column('user', sqlalchemy.Integer,
#                       sqlalchemy.ForeignKey('users.id')),
#     sqlalchemy.Column('request', sqlalchemy.Integer,
#                       sqlalchemy.ForeignKey('requests.id'))
# )


class Request(SqlAlchemyBase):
    __tablename__ = 'requests'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sender_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    provider_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
