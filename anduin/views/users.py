from flask import Blueprint

from anduin.controllers import users as users_controller
from anduin.exceptions import RowNotFound

users_blueprint = Blueprint('users_blueprint', __name__, url_prefix='/api/users')


@users_blueprint.route('/', methods=['GET'])
def get_users():
    users = users_controller.get_users()
    return {'users': users}, 200


@users_blueprint.route('/<id>', methods=['GET'])
def get_user_by_id(id):
    try:
        user = users_controller.get_user_by_id(id)
        return {'user': user}, 200
    except RowNotFound:
        return {'error': f'No user found with id {id}'}, 404


@users_blueprint.route('/<id>/inventory', methods=['GET'])
def get_user_inventory_by_id(id):
    try:
        inventory = users_controller.get_user_inventory_by_id(id)
        return {'inventory': inventory}, 200
    except RowNotFound:
        return {'error': f'No user found with id {id}'}, 404
