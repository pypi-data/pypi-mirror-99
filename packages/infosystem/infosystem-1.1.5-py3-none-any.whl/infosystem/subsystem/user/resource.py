import uuid
from sqlalchemy import orm
from infosystem.database import db
from sqlalchemy import UniqueConstraint
from infosystem.common.subsystem import entity


class User(entity.Entity, db.Model):

    SYSADMIN_USERNAME = 'sysadmin'

    attributes = ['domain_id', 'name', 'email', 'nickname', 'photo_id']
    attributes += entity.Entity.attributes

    domain_id = db.Column(
        db.CHAR(32), db.ForeignKey('domain.id'), nullable=False)
    domain = orm.relationship('Domain', backref=orm.backref('users'))
    name = db.Column(db.String(80), nullable=False)
    nickname = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(
        db.String(64), nullable=False, default=uuid.uuid4().hex)
    photo_id = db.Column(db.CHAR(32), db.ForeignKey('image.id'), nullable=True)

    __table_args__ = (
        UniqueConstraint('name', 'domain_id', name='user_name_domain_id_uk'),
        UniqueConstraint(
            'email', 'domain_id', name='user_email_domain_id_uk'),)

    def __init__(self, id, domain_id, name, email,
                 nickname=None, photo_id=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.domain_id = domain_id
        self.name = name
        self.email = email
        # self.password = password
        self.nickname = nickname
        self.photo_id = photo_id
