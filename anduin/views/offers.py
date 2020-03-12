from flask import Blueprint, request

from anduin.controllers import offers as offers_controller

offers_blueprint = Blueprint('offers_blueprint', __name__, url_prefix='/api/offers')


@offers_blueprint.route('/<id>', methods=['GET'])
def get_offer_by_id(id):
    offer = offers_controller.get_offer_by_id(id)
    return {'offer': offer}, 200


@offers_blueprint.route('/', methods=['POST'])
def create_offer():
    req_body = request.get_json()
    created = offers_controller.create_offer(req_body)
    return {'offer': created}, 201


@offers_blueprint.route('/<id>/accept', methods=['POST'])
def accept_offer_by_id(id):
    updated = offers_controller.accept_offer_by_id(id)
    return {'offer': updated}, 200


@offers_blueprint.route('/<id>/reject', methods=['POST'])
def reject_offer_by_id(id):
    updated = offers_controller.reject_offer_by_id(id)
    return {'offer': updated}, 200
