import csv
import os
from collections import defaultdict

from sqlalchemy.exc import SQLAlchemyError

from anduin.constants import OFFER_STATUS_ACCEPTED, OFFER_STATUS_PENDING, OFFER_STATUS_REJECTED
from anduin.database import db
from anduin.models.offers import Offers
from anduin.models.users import Users
from anduin.models.weapons import Weapons


def run():
    LOCAL_DIRNAME = os.path.dirname(__file__)
    USERS_FILE_PATH = os.path.join(LOCAL_DIRNAME, 'data/users.csv')
    WEAPONS_FILE_PATH = os.path.join(LOCAL_DIRNAME, 'data/weapons.csv')

    created_users_by_username = {}
    created_weapons_by_username = defaultdict(list)

    # Backfill users
    with open(USERS_FILE_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            user = Users(
                username=row['username'],
                race=row['race']
            ).save(flush_only=True)
            created_users_by_username[user.username] = user

    # Backfill weapons
    with open(WEAPONS_FILE_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            weapon = Weapons(
                category=row['category'],
                owner=created_users_by_username[row['username']].id
            ).save(flush_only=True)
            created_weapons_by_username[row['username']].append(weapon)

    # Create some hardcoded offers
    offer_1 = Offers(status=OFFER_STATUS_PENDING).save(flush_only=True)
    offer_1.users = [created_users_by_username['gandalf1'], created_users_by_username['galadariel']]
    offer_1.weapons = [
        created_weapons_by_username['gandalf1'][0],
        created_weapons_by_username['gandalf1'][1],
        created_weapons_by_username['galadariel'][2],
    ]

    offer_2 = Offers(status=OFFER_STATUS_ACCEPTED).save(flush_only=True)
    offer_2.users = [created_users_by_username['jigglypuff'], created_users_by_username['pugglyjiff']]
    offer_2.weapons = [
        created_weapons_by_username['jigglypuff'][0],
        created_weapons_by_username['pugglyjiff'][0]
    ]

    offer_3 = Offers(status=OFFER_STATUS_REJECTED).save(flush_only=True)
    offer_3.users = [created_users_by_username['legoless'], created_users_by_username['g!ml!']]
    offer_3.weapons = [
        created_weapons_by_username['legoless'][0],
        created_weapons_by_username['legoless'][1],
        created_weapons_by_username['g!ml!'][0]
    ]

    offer_4 = Offers(status=OFFER_STATUS_PENDING).save(flush_only=True)
    offer_4.users = [created_users_by_username['legoless'], created_users_by_username['g!ml!']]
    offer_4.weapons = [
        created_weapons_by_username['legoless'][0],
        created_weapons_by_username['legoless'][1],
        created_weapons_by_username['g!ml!'][0]
    ]

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        print(f'Error committing to db: {str(e)}')
        raise
