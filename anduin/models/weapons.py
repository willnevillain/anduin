import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates

from anduin.models.base_model import BaseModel

WEAPONS_VARIANTS = ['Sword', 'Staff', 'Axe']


class Weapons(BaseModel):
    variant = sa.Column(sa.String, nullable=False)
    owner = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))

    @validates('variant')
    def validate_vairant(self, key, variant):
        assert variant in WEAPONS_VARIANTS
        return variant
