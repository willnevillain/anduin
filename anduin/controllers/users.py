from anduin.exceptions import RowNotFound
from anduin.models.users import Users


def get_users():
    """
    Get all Users from db and return as dicts
    """
    return [user.to_dict() for user in Users.get().all()]


def get_user_by_id(id):
    """
    Get a Users row from db and return as dict
    :param id: id of row in users table
    :type id: uuid str
    """
    user = Users.get_by_id(id).first()
    if not user:
        raise RowNotFound()
    return user.to_dict()


def get_user_inventory_by_id(id):
    """
    Get a Users row from db and its weapons inventory as dicts
    :param id: id of row in users table
    :type id: uuid str
    """
    user = Users.get_by_id(id).first()
    if not user:
        raise RowNotFound()
    return [weapon.to_dict(recurse_relationships=False) for weapon in user.weapons]
