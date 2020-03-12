from factory import Sequence
from factory.alchemy import SQLAlchemyModelFactory

from anduin.constants import OFFER_STATUS_PENDING, RACE_ELF, WEAPON_AXE
from anduin.database import db
from anduin.models.offers import Offers
from anduin.models.users import Users
from anduin.models.weapons import Weapons


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'flush'


class OffersFactory(BaseFactory):
    class Meta:
        model = Offers

    status = OFFER_STATUS_PENDING


class UsersFactory(BaseFactory):
    class Meta:
        model = Users

    username = Sequence(lambda n: f'user_{n}')
    race = RACE_ELF


class WeaponsFactory(BaseFactory):
    class Meta:
        model = Weapons

    category = WEAPON_AXE
