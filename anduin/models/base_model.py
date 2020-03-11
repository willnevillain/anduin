import datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from anduin.app import db

class BaseModel(db.Model):
    __abstract__ = True

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
