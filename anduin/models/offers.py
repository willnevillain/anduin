import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates

from anduin.constants import OFFER_STATUS_PENDING, OFFER_STATUSES
from anduin.models.base_model import BaseModel


offers_users_association_table = sa.Table(
    'offers_users_association_table',
    BaseModel.metadata,
    sa.Column('offers_id', UUID(as_uuid=True), sa.ForeignKey('offers.id')),
    sa.Column('users_id', UUID(as_uuid=True), sa.ForeignKey('users.id')),
)

offers_weapons_association_table = sa.Table(
    'offers_weapons_association_table',
    BaseModel.metadata,
    sa.Column('offers_id', UUID(as_uuid=True), sa.ForeignKey('offers.id')),
    sa.Column('weapons_id', UUID(as_uuid=True), sa.ForeignKey('weapons.id')),
)


class Offers(BaseModel):
    __tablename__ = 'offers'

    status = sa.Column(sa.String, nullable=False, default=OFFER_STATUS_PENDING)

    users = relationship('Users', secondary=offers_users_association_table, backref='offers')
    weapons = relationship('Weapons', secondary=offers_weapons_association_table, backref='offers')

    @validates('status')
    def validate(self, key, status):
        assert status in OFFER_STATUSES
        return status
