#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.store import StoreModel
from models.user import UserModel
from utils.date_format import getTimeStamp


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('store_name',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('cookies',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('csrf_token',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('status',
                        type=int,
                        required=True,
                        help="This field cannot be blank."
                        )

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()

        storeName = data['store_name']
        description = data["description"]
        cookies = data["cookies"]
        csrf_token = data["csrf_token"] if "csrf_token" in data else None
        status = data["status"]

        if StoreModel.find_by_name(storeName):
            return {
                       "status": 400,
                       "data": None,
                       'message': "Store name '{}' has exists.".format(storeName)
                   }, 400
        else:
            store = StoreModel(storeName, description, cookies, csrf_token, status, getTimeStamp(), None, None, None)
            store.save_to_db()

            return {
                       "status": 201,
                       "data": store.json(),
                       "message": "Store '{}' create successfully.".format(storeName)
                   }, 201


class StoreList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        stores = [store.json() for store in StoreModel.find_all()]

        if user_id:
            return {
                       "status": 200,
                       "message": "Get success list",
                       "data": [store for store in stores],
                       "total": len(StoreModel.find_all())
                   }, 200


class StoreItem(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('cookies',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('csrf_token',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('status',
                        type=int,
                        required=True,
                        help="This field cannot be blank."
                        )

    @jwt_required()
    def get(self, store_id: int):
        item = StoreModel.find_by_id(store_id)
        if not item:
            return {
                       "status": 404,
                       "data": None,
                       'message': 'The item does not exist'
                   }, 404

        return {
                   "status": 200,
                   "data": item.json(),
                   "message": "Success"
               }, 200

    @jwt_required()
    def put(self, store_id: int):
        item = StoreModel.find_by_id(store_id)

        if item is None:
            return {
                       "status": 404,
                       "data": None,
                       'message': "The item id '{}' does not exist.".format(store_id)
                   }, 404

        # Save to log table
        userId = get_jwt_identity()
        user = UserModel.find_by_id(userId)
        username = user.username

        data = self.parser.parse_args()

        cookies = data["cookies"]
        csrf_token = data["csrf_token"]
        status = data["status"]

        item.cookies = cookies
        item.csrf_token = csrf_token
        item.status = status
        item.updated_at = getTimeStamp()
        item.updated_by = username

        item.save_to_db()

        return {
                   "status": 200,
                   "message": "Success",
                   "data": item.json()
               }, 200
