import datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.collections import InstrumentedList

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

    def to_dict(self, recurse_relationships=True):
        """
        Returns dictionary representation of object. Relationships are recursed and converted to dicts if specified.
        :param recurse_relationships: whether or not to recurse and convert relationship objects to dicts.
        :type recurse_relationships: Boolean
        """
        model_dict = {}
        for column in self.__table__.columns:
            model_dict[column.name] = getattr(self, column.name)
        if recurse_relationships:
            for rel in self.__mapper__.relationships.keys():
                rel_result = getattr(self, rel)
                if type(rel_result) == InstrumentedList:  # If it's a many relationship, we get a list
                    model_dict[rel] = [model.to_dict(recurse_relationships=False) for model in rel_result]
                else:  # Else we get a single model
                    model_dict[rel] = rel_result.to_dict()
        return model_dict
