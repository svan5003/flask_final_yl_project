from data import db_session
from data.users import User

db_session.global_init("db/users_requests.sqlite")
session = db_session.create_session()
user = session.query(User).first()
print(user.outgoing_requests[0].name)