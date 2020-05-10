from flask import jsonify
from flask_restful import Resource, reqparse, abort
from data.users import User
from data import db_session


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    request = session.query(User).get(user_id)
    if not request:
        abort(404, message=f"User {user_id} not found")


def to_dict(user):
    return {"name": user.name,
            "surname": user.surname,
            "about": user.about,
            "address": user.address,
            "telephone_number": user.telephone_number,
            "email": user.email
            }


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': to_dict(user)})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        args = parser_user.parse_args()
        if args['name']:
            user.name = args['name']
        if args['surname']:
            user.surname = args['surname']
        if args['address']:
            user.address = args['address']
        if args['about']:
            user.about = args['about']
        if args['telephone_number']:
            user.telephone_number = args['telephone_number']
        if args['email']:
            user.email = args['email']
        if args['password']:
            user.set_password(args['password'])
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'user': [to_dict(item) for item in users]})

    def post(self):
        args = parser_user_list.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            surname=args['surname'],
            about=args['about'],
            address=args['address'],
            telephone_number=args['telephone_number'],
            email=args['email']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


# парсер аргументов для класса UserListResource
# используется для добавления пользователя
parser_user_list = reqparse.RequestParser()
parser_user_list.add_argument('name', required=True)
parser_user_list.add_argument('surname', required=True)
parser_user_list.add_argument('about', required=True)
parser_user_list.add_argument('address', required=True, type=dict)
parser_user_list.add_argument('email', required=True)
parser_user_list.add_argument('telephone_number', required=True)
parser_user_list.add_argument('password', required=True)

# парсер аргументов для класса UserResource
# используется для редактирования пользователя
parser_user = reqparse.RequestParser()
parser_user.add_argument('name')
parser_user.add_argument('surname')
parser_user.add_argument('about')
parser_user.add_argument('address', type=dict)
parser_user.add_argument('email')
parser_user.add_argument('telephone_number')
parser_user.add_argument('password')
