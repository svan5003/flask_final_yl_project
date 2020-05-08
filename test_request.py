from data import db_session
from data.users import User
from data.requests import Request

db_session.global_init("db/users_requests.sqlite")
session = db_session.create_session()
user = session.query(User).first()
session = db_session.create_session()
request = Request()
request.name = "вскопать грядку"
request.description = "ааааааааааа"
request.is_active = True
request.sender_id = user.id
request.address = ", ".join(["Сочи", "Дарвина", "93", "67"])
session.commit()