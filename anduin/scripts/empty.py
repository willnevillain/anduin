from flask import current_app

from anduin.constants import ENV_PROD
from anduin.database import db
from anduin.models.offers import Offers
from anduin.models.users import Users
from anduin.models.weapons import Weapons


def run():
    if current_app.config['ENV'] != ENV_PROD:
        offers = db.session.query(Offers)
        for offer in offers:
            offer.users = []
            offer.weapons = []
            offer.delete()
        db.session.query(Weapons).delete()
        db.session.query(Users).delete()
        db.session.commit()
