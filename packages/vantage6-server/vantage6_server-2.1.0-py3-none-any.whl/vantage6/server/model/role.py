from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound

from vantage6.server.model.base import Base, Database


class Role(Base):
    """Collection of Rules
    """

    # fields
    name = Column(Text)
    description = Column(Text)
    organization_id = Column(Integer, ForeignKey("organization.id"))

    # relationships
    rules = relationship("Rule", back_populates="roles",
                         secondary="role_rule_association")
    organization = relationship("Organization", back_populates="roles")
    users = relationship("User", back_populates="roles",
                         secondary="Permission")

    @classmethod
    def get_by_name(cls, name):
        session = Database().Session
        try:
            return session.query(cls).filter_by(name=name).first()
        except NoResultFound:
            return None

    def __repr__(self):
        return (
            f"<Role {self.id}, "
            f"name: {self.name}, "
            f"description: {self.description}, "
            f"users: {len(self.users)}"
            ">"
        )
