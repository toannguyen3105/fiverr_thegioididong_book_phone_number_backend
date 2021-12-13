#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import UserModel
from utils.date_format import getTimeStamp


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = self.parser.parse_args()
        username = data['username']
        password = generate_password_hash(data["password"])

        if UserModel.find_by_username(username):
            return {
                       "status": 400,
                       "data": None,
                       'message': "Username '{}' has existed.".format(username)
                   }, 400
        else:
            user = UserModel(username, password, getTimeStamp(), None, None, None)
            user.save_to_db()

            return {
                       "status": 201,
                       "data": user.json(),
                       "message": "'{}' create successfully.".format(username)
                   }, 201


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = self.parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user and check_password_hash(user.password, data['password']):
            expires = timedelta(days=1)
            access_token = create_access_token(identity=user.id, expires_delta=expires, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        else:
            return {
                       "status": 401,
                       "data": None,
                       "message": "Wrong information"
                   }, 401


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class UserProfile(Resource):
    @jwt_required()
    def get(self):
        # Access the identity of the current user with get_jwt_identity
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        return {
                   "status": 200,
                   "message": "Success",
                   "data": user.json()
               }, 200
