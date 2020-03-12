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
    :param id: id of row in Users table
    :type id: uuid str
    """
    user = Users.get_by_id(id).first()
    if not user:
        raise RowNotFound(f'No user found with id {id}')
    return user.to_dict()


def get_user_by_username(username):
    """
    Get a Users row from db by username and return as dict
    :param username: username of row in Users table
    :type username: str
    """
    user = Users.get_by_username(username).first()
    if not user:
        raise RowNotFound(f'No user found with username {username}')
    return user.to_dict()


def get_user_inventory_by_id(id):
    """
    Get a Users row from db and its weapons inventory as dicts
    :param id: id of row in users table
    :type id: uuid str
    """
    user = Users.get_by_id(id).first()
    if not user:
        raise RowNotFound(f'No user found with id {id}')
    return [weapon.to_dict(recurse_relationships=False) for weapon in user.weapons]
