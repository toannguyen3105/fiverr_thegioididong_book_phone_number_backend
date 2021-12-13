#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import db
from utils.date_format import getTimeStringFromTimeStamp


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, comment="Account to login")
    password = db.Column(db.String(200), nullable=False, comment="Password of account")
    created_at = db.Column(db.Integer, nullable=True, comment="Timestamp create user")
    created_by = db.Column(db.String(30), nullable=True, comment="Person create user")
    updated_at = db.Column(db.Integer, nullable=True, comment="Timestamp update user")
    updated_by = db.Column(db.String(30), nullable=True, comment="Person update user")

    def __init__(self, username, password, created_at, created_by, updated_at, updated_by):
        self.username = username
        self.password = password
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at,
            'created_at_string': None if self.created_at is None else getTimeStringFromTimeStamp(self.created_at),
            'created_by': self.created_by,
            'updated_at': self.updated_at,
            'updated_at_string': None if self.updated_at is None else getTimeStringFromTimeStamp(self.updated_at),
            'updated_by': self.updated_by,
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
