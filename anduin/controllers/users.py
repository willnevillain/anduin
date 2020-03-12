from anduin.models.users import Users


def get_users():
    """
    Get all Users from db and return as dicts
    """
    return [user.to_dict() for user in Users.get().all()]


def get_user_by_id(id):
    """
    Get a Users from db and return as dicts
    """
    return Users.get_by_id(id).one().to_dict()


def get_user_inventory_by_id(id):
    weapons = Users.get_by_id(id).one().weapons
    return [weapon.to_dict(recurse_relationships=False) for weapon in weapons]
