from flask import Blueprint

offers_blueprint = Blueprint('offers_blueprint', __name__, url_prefix='/api/offers')


@offers_blueprint.route('/<id>', methods=['GET'])
def get_offer_by_id(id):
    return {}, 200


@offers_blueprint.route('/', methods=['POST'])
def create_offer():
    return {}, 200


@offers_blueprint.route('/<id>/accept', methods=['POST'])
def accept_offer_by_id(id):
    return {}, 200


@offers_blueprint.route('/<id>/reject', methods=['POST'])
def reject_offer_by_id(id):
    return {}, 200
