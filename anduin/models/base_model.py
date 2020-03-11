import datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from anduin.database import db


class BaseModel(db.Model):
    """Base model with consistent default columns"""
    __abstract__ = True

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def get(cls):
        """
        Get all rows from table
        """
        return db.session.query(cls)

    @classmethod
    def get_by_id(cls, id):
        """
        Get a row by id.
        :param id: uuid
        """
        return db.session.query(cls).filter(cls.id == id)

    def save(self, flush_only=False):
        """
        Add model to session and either flushes to DB or commits.
        :param session: flask_sqlalchemy session object
        :param flush_only: whether to just flush or to fully commit to DB
        :type session flask_sqlalchemy.scoped_session
        :type flush_only: Boolean
        """
        db.session.add(self)
        db.session.flush() if flush_only else db.session.commit()
        return self

    def delete(self):
        """
        Delete model.
        """
        db.session.delete(self)
        db.session.commit()
