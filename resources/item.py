#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from decouple import config
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from utils.csgoempire.header import generate_header_for_get_request
from utils.csgoempire.item_info import get_trades_list
from utils.buffmarket.header import buff_market_get_header
from utils.buffmarket.item import get_trades_list_buff_market
from utils.buff163.header import buff_163_get_header
from utils.buff163.item import get_trades_list_buff_163, get_trades_dota2_list_buff_163
from utils.date_format import getTimeStamp
from utils.telegram.send_message import send_message_telegram

MARK_UP_PRICE = config('MARK_UP_PRICE')
DISCOUNT_PRICE = config('DISCOUNT_PRICE')
CSGO_EMPIRE_MARKET_BASE_URL = config('CSGO_EMPIRE_MARKET_BASE_URL')
BUFF_MARKET_BASE_URL = config('BUFF_MARKET_BASE_URL')
BUFF_163_BASE_URL = config('BUFF_163_BASE_URL')


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('goods_id',
                        type=int,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('min_price',
                        type=float,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('max_price',
                        type=float,
                        required=True,
                        help="This field cannot be blank."
                        )

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()

        store_id = data['store_id']
        goods_id = data['goods_id']
        name = data["name"]
        price = data["price"]
        min_price = data["min_price"]
        max_price = data["max_price"]

        # Save to item table
        item = ItemModel(goods_id, name, price, min_price, max_price, store_id, getTimeStamp(), None, None, None)
        item.save_to_db()

        return {
                   "status": 201,
                   "data": item.json(),
                   "message": "'{}' order successfully".format(name)
               }, 201


class ItemAction(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('min_price',
                        type=float,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('max_price',
                        type=float,
                        required=True,
                        help="This field cannot be blank."
                        )

    @jwt_required()
    def get(self, item_id: int):
        item = ItemModel.find_by_id(item_id)
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
    def put(self, item_id: int):
        item = ItemModel.find_by_id(item_id)

        if item is None:
            return {
                       "status": 404,
                       "data": None,
                       'message': "The item id '{}' does not exist.".format(item_id)
                   }, 404

        # Save to log table
        userId = get_jwt_identity()
        user = UserModel.find_by_id(userId)
        username = user.username

        data = self.parser.parse_args()

        min_price = data["min_price"]
        max_price = data["max_price"]

        item.min_price = min_price
        item.max_price = max_price
        item.updated_at = getTimeStamp()
        item.updated_by = username

        item.save_to_db()

        return {
                   "status": 200,
                   "message": "Success",
                   "data": item.json()
               }, 200


class ItemList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]

        if user_id:
            return {
                       "status": 200,
                       "message": "Get success list",
                       "data": [item for item in items],
                       "total": len(ItemModel.find_all())
                   }, 200


class ItemFetch(Resource):
    @jwt_required()
    def get(self):
        # delete items
        ItemModel.delete_all()

        # store list
        stores = StoreModel.find_all()

        # fetch csgo
        status = [store.status for store in stores if store.store_name == "CSGO_EMPIRE"][0]
        if status == 1:
            cookies = [store.cookies for store in stores if store.store_name == "CSGO_EMPIRE"][0]
            store_id = [store.id for store in stores if store.store_name == "CSGO_EMPIRE"][0]
            headers = generate_header_for_get_request(cookies)
            payload = {}
            trades_list = get_trades_list(requests, CSGO_EMPIRE_MARKET_BASE_URL, headers, payload)
            send_message_telegram(f"FETCH CSGO_EMPIRE total: {len(trades_list)} items")

            for tradeItem in trades_list:
                goods_id = tradeItem["item_id"]
                market_name = tradeItem["items"][0]["market_name"]
                price = tradeItem["total_value"]
                min_price = round(price - (price * float(DISCOUNT_PRICE) / 100), 2)
                max_price = price
                item = ItemModel(goods_id, market_name, price, min_price, max_price, store_id, getTimeStamp(), None, None,
                                 None)
                item.save_to_db()

        # fetch buffmarket
        # cookies = [store.cookies for store in stores if store.store_name == "BUFF_MARKET"][0]
        # csrf_token = [store.csrf_token for store in stores if store.store_name == "BUFF_MARKET"][0]
        # store_id = [store.id for store in stores if store.store_name == "BUFF_MARKET"][0]
        # headers = buff_market_get_header(cookies, csrf_token)
        # payload = {}
        # trades_list = get_trades_list_buff_market(requests, BUFF_MARKET_BASE_URL, headers, payload)
        # send_message_telegram(f"FETCH BUFF_MARKET total: {len(trades_list['items'])} items")
        #
        # for tradeItem in trades_list["items"]:
        #     goods_id = tradeItem["id"]
        #     market_name = trades_list["goods_infos"][str(tradeItem['goods_id'])]["market_hash_name"]
        #     price = float(tradeItem["price"])
        #     min_price = round(price - (price * float(DISCOUNT_PRICE) / 100), 2)
        #     max_price = price
        #     item = ItemModel(goods_id, market_name, price, min_price, max_price, store_id, getTimeStamp(), None,
        #                      None,
        #                      None)
        #     item.save_to_db()

        # fetch buff163
        status = [store.status for store in stores if store.store_name == "BUFF163"][0]
        if status == 1:
            cookies = [store.cookies for store in stores if store.store_name == "BUFF163"][0]
            store_id = [store.id for store in stores if store.store_name == "BUFF163"][0]
            headers = buff_163_get_header(cookies)
            payload = {}
            trades_list = get_trades_list_buff_163(requests, BUFF_163_BASE_URL, headers, payload)
            send_message_telegram(f"FETCH BUFF_163 total: {len(trades_list['items'])} items")

            for tradeItem in trades_list["items"]:
                goods_id = tradeItem["id"]
                market_name = trades_list["goods_infos"][str(tradeItem['goods_id'])]["market_hash_name"]
                price = float(tradeItem["price"])
                min_price = round(price - (price * float(DISCOUNT_PRICE) / 100), 2)
                max_price = price
                item = ItemModel(goods_id, market_name, price, min_price, max_price, store_id, getTimeStamp(), None,
                                 None,
                                 None)
                item.save_to_db()

            trades_list = get_trades_dota2_list_buff_163(requests, BUFF_163_BASE_URL, headers, payload)
            send_message_telegram(f"FETCH BUFF_163 total: {len(trades_list['items'])} items")

            for tradeItem in trades_list["items"]:
                goods_id = tradeItem["id"]
                market_name = trades_list["goods_infos"][str(tradeItem['goods_id'])]["market_hash_name"]
                price = float(tradeItem["price"])
                min_price = round(price - (price * float(DISCOUNT_PRICE) / 100), 2)
                max_price = price
                item = ItemModel(goods_id, market_name, price, min_price, max_price, store_id, getTimeStamp(), None,
                                 None,
                                 None)
                item.save_to_db()

        return {
                   "status": 200,
                   "message": "Fetch success",
                   "data": None
               }, 200
