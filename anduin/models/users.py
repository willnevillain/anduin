import sqlalchemy as sa
from sqlalchemy.orm import relationship, validates

from anduin.models.base_model import BaseModel

RACES = ['Elf', 'Wizards', 'Dwarves']


class Users(BaseModel):
    username = sa.Column(sa.String, unique=True, nullable=False)
    race = sa.Column(sa.String, nullable=False)

    weapons = relationship('Weapons', backref='user')

    @validates('race')
    def validate_race(self, key, race):
        assert race in RACES
        return race
