import bcrypt

from sqlalchemy import Column, String, Integer, ForeignKey, exists
from sqlalchemy.orm import relationship, validates

from vantage6.server.model.base import Database
from vantage6.server.model.authenticable import Authenticatable


class User(Authenticatable):
    """User (person) that can access the system.

    Users always belong to an organization and can have certain
    rights within an organization.
    """
    _hidden_attributes = ['password']

    # overwrite id with linked id to the authenticatable
    id = Column(Integer, ForeignKey('authenticatable.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'user',
    }

    # fields
    username = Column(String, unique=True)
    password = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)
    roles = Column(String)
    organization_id = Column(Integer, ForeignKey("organization.id"))

    # relationships
    organization = relationship("Organization", back_populates="users")
    roles = relationship("Role", back_populates="users",
                         secondary="Permission")
    rules = relationship("Rule", back_populates="users",
                         secondary="UserPermission")

    def __repr__(self):
        organization = self.organization.name if self.organization else "None"
        return (
            f"<User "
            f"id={self.id}, username='{self.username}', roles='{self.roles}', "
            f"organization='{organization}'"
            f">"
        )

    @validates("password")
    def _validate_password(self, key, password):
        return self.hash_password(password)

    @staticmethod
    def hash_password(password: str):
        return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())\
            .decode('utf8')

    def set_password(self, pw):
        self.password = pw

    def check_password(self, pw):
        if self.password is not None:
            expected_hash = self.password.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False

    @classmethod
    def get_by_username(cls, username):
        session = Database().Session
        return session.query(cls).filter_by(username=username).one()

    @classmethod
    def get_by_email(cls, email):
        session = Database().Session
        return session.query(cls).filter_by(email=email).one()

    @classmethod
    def get_user_list(cls, filters=None):
        session = Database().Session
        return session.query(cls).all()

    @classmethod
    def username_exists(cls, username):
        session = Database().Session
        return session.query(exists().where(cls.username == username)).scalar()

    @classmethod
    def exists(cls, field, value):
        session = Database().Session
        return session.query(exists().where(getattr(cls, field) == value))\
            .scalar()
