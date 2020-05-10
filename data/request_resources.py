from flask import jsonify
from flask_restful import Resource, reqparse, abort
from data.requests import Request
from data import db_session


def abort_if_request_not_found(request_id):
    session = db_session.create_session()
    request = session.query(Request).get(request_id)
    if not request:
        abort(404, message=f"Request {request_id} not found")


def to_dict(request):
    return {"name": request.name,
            "description": request.description,
            "address": request.address,
            "sender_id": request.sender_id,
            "provider_id": request.provider_id,
            "is_active": request.is_active}


class RequestResource(Resource):
    def get(self, request_id):
        abort_if_request_not_found(request_id)
        session = db_session.create_session()
        request = session.query(Request).get(request_id)
        return jsonify({'request': to_dict(request)})

    def put(self, request_id):
        abort_if_request_not_found(request_id)
        session = db_session.create_session()
        request = session.query(Request).get(request_id)
        args = parser_req.parse_args()
        if args['name']:
            request.name = args['name']
        if args['description']:
            request.description = args['description']
        if args['address']:
            request.address = args['address']
        if args['sender_id']:
            request.sender_id = args['sender_id']
        if args['provider_id']:
            request.provider_id = args['provider_id']
        if args['is_active'] is True or args['is_active'] is False:
            request.is_active = args['is_active']
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, request_id):
        abort_if_request_not_found(request_id)
        session = db_session.create_session()
        request = session.query(Request).get(request_id)
        session.delete(request)
        session.commit()
        return jsonify({'success': 'OK'})


class RequestListResource(Resource):
    def get(self):
        session = db_session.create_session()
        requests = session.query(Request).all()
        return jsonify({'requests': [to_dict(item) for item in requests]})

    def post(self):
        args = parser_req_list.parse_args()
        session = db_session.create_session()
        request = Request(
            name=args['name'],
            description=args['description'],
            address=args['address'],
            sender_id=args['sender_id'],
            provider_id=args.get('provider_id'),
            is_active=args["is_active"]
        )
        session.add(request)
        session.commit()
        return jsonify({'success': 'OK'})


# парсер аргументов для класса RequestListResource
# используется для добавления новости
parser_req_list = reqparse.RequestParser()
parser_req_list.add_argument('name', required=True)
parser_req_list.add_argument('description', required=True)
parser_req_list.add_argument('address', required=True)
parser_req_list.add_argument('is_active', required=True, type=bool)
parser_req_list.add_argument('provider_id', type=int)
parser_req_list.add_argument('sender_id', required=True, type=int)

# парсер аргументов для класса RequestResource
# используется для редактирования новости
parser_req = reqparse.RequestParser()
parser_req.add_argument('name')
parser_req.add_argument('description')
parser_req.add_argument('address')
parser_req.add_argument('is_active', type=bool)
parser_req.add_argument('provider_id', type=int)
parser_req.add_argument('sender_id', type=int)
