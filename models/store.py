#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import db
from utils.date_format import getTimeStringFromTimeStamp


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(30), nullable=False, comment="Store name")
    description = db.Column(db.String(100), nullable=False, comment="Description")
    cookies = db.Column(db.String(600), nullable=False, comment="Cookies user login")
    csrf_token = db.Column(db.String(200), nullable=True, comment="CSRF TOKEN user login")
    status = db.Column(db.Integer, nullable=False, comment="Status")
    created_at = db.Column(db.Integer, nullable=True, comment="Timestamp")
    created_by = db.Column(db.String(30), nullable=True, comment="Person create user")
    updated_at = db.Column(db.Integer, nullable=True, comment="Timestamp")
    updated_by = db.Column(db.String(30), nullable=True, comment="Person update user")

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, store_name, description, cookies, csrf_token, status, created_at, created_by, updated_at,
                 updated_by):
        self.store_name = store_name
        self.description = description
        self.cookies = cookies
        self.csrf_token = csrf_token
        self.status = status
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by

    def json(self):
        return {
            'id': self.id,
            'store_name': self.store_name,
            'description': self.description,
            'cookies': self.cookies,
            'csrf_token': self.csrf_token,
            'status': self.status,
            'created_at': self.created_at,
            'created_at_string': None if self.created_at is None else getTimeStringFromTimeStamp(self.created_at),
            'created_by': self.created_by,
            'updated_at': self.updated_at,
            'updated_at_string': None if self.updated_at is None else getTimeStringFromTimeStamp(self.updated_at),
            'updated_by': self.updated_by,
            'items': [item.json() for item in self.items.all()]
        }

    @classmethod
    def find_by_name(cls, store_name):
        return cls.query.filter_by(store_name=store_name).first()

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
