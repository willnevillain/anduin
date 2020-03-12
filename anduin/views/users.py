from flask import Blueprint

users_blueprint = Blueprint('users_blueprint', __name__, url_prefix='/api/users')


@users_blueprint.route('/', methods=['GET'])
def get_users():
    return {}, 200


@users_blueprint.route('/<id>', methods=['GET'])
def get_user_by_id(id):
    return {}, 200


@users_blueprint.route('/<id>/inventory', methods=['GET'])
def get_user_inventory_by_id(id):
    return {}, 200
