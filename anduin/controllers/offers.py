from anduin.constants import OFFER_STATUS_ACCEPTED, OFFER_STATUS_PENDING, OFFER_STATUS_REJECTED
from anduin.exceptions import RowNotFound, InvalidDataIntegrity
from anduin.models.offers import Offers
from anduin.models.users import Users
from anduin.models.weapons import Weapons


def get_offer_by_id(id):
    """
    Get an Offers row from db and return as dict
    :param id: id of row in users table
    :type id: uuid str
    """
    offer = Offers.get_by_id(id).first()
    if not offer:
        raise RowNotFound()
    return offer.to_dict()


def create_offer(offer_dict):
    """
    Create a new Offers row in DB
    :param offer_dict: dict of values for new Offer
    :type offer_dict: dict
    {
      'users': [
        {
          'username': <username>,
          'weapon_ids': [<id>, <id>]
        },
        {
          'username': <username>,
          'weapon_ids': [<id>, <id>]
        }
      ]
    }
    """
    try:
        _validate_new_offer(offer_dict)
    except (RowNotFound, InvalidDataIntegrity):
        raise
    user_models = []
    weapon_models = []
    for user in offer_dict['users']:
        user_models.append(Users.get_by_username(user['username']).first())
        for weapon_id in user['weapon_ids']:
            weapon_models.append(Weapons.get_by_id(weapon_id).first())
    offer = Offers()
    offer.users = user_models
    offer.weapons = weapon_models
    offer.save()
    return offer.to_dict()


def accept_offer_by_id(id):
    """
    Change status of an offer to be accepted.
    Note: the author assumes that ownership of items does not immediately change on an accepted offer
    :param id: id of row on Offers table
    :type id: uuid str
    """
    return _update_offer_status_by_id(id, OFFER_STATUS_ACCEPTED)


def reject_offer_by_id(id):
    """
    Change status of an offer to be rejected.
    Note: the author assumes that ownership of items does not immediately change on an accepted offer
    :param id: id of row on Offers table
    :type id: uuid str
    """
    return _update_offer_status_by_id(id, OFFER_STATUS_REJECTED)


def _update_offer_status_by_id(id, new_status):
    offer = Offers.get_by_id(id).first()
    if not offer:
        raise RowNotFound()
    elif offer.status != OFFER_STATUS_PENDING:
        raise InvalidDataIntegrity()
    offer.status = new_status
    offer.save()
    return offer.to_dict()


def _validate_new_offer(offer_dict):
    """
    Validate that all usernames and weapon ids passed in are valid and match current DB state.
    :param offer_dict: dict of values for new Offer
    :type offer_dict: dict
    {
      'users': [
        {
          'username': <username>,
          'weapon_ids': [<id>, <id>]
        },
        {
          'username': <username>,
          'weapon_ids': [<id>, <id>]
        }
      ]
    }
    """
    for user in offer_dict['users']:
        user_model = Users.get_by_username(user['username']).first()
        if not user_model:
            raise RowNotFound()
        user_model_weapon_ids = [weapon.id for weapon in user_model.weapons]
        for weapon_id in user['weapon_ids']:
            weapon_model = Weapons.get_by_id(weapon_id).first()
            if not weapon_model:
                raise RowNotFound()
            elif weapon_model.id not in user_model_weapon_ids:
                raise InvalidDataIntegrity()
