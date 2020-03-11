import datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel(Base):
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
