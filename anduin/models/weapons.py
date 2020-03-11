import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates

from anduin.constants import WEAPON_CATEGORIES
from anduin.models.base_model import BaseModel


class Weapons(BaseModel):
    category = sa.Column(sa.String, nullable=False)
    owner = sa.Column(UUID(as_uuid=True), sa.ForeignKey('users.id'))

    @validates('category')
    def validate_category(self, key, category):
        assert category in WEAPON_CATEGORIES
        return category
