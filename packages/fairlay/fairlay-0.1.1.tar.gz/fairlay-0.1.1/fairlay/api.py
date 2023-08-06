from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
import socket
import gzip
from enum import Enum
import datetime
import arrow
import httpx
import time
import random
import base64
import ujson
from marshmallow import Schema, fields, ValidationError, validates, INCLUDE
from marshmallow_enum import EnumField
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from .utils import pubkey_xml_to_pem, pubkey_pem_to_xml

def convert_ticks_to_datetime(s):
    return datetime.datetime(1, 1, 1) + datetime.timedelta(microseconds=int(s)/10)


class MarketCategory(Enum):
    all = 0
    soccer = 1
    tennis = 2
    golf = 3
    cricket = 4
    rugbyunion = 5
    boxing = 6
    horseracing = 7
    Motorsport = 8
    special = 10
    rugbyleague = 11
    basketball = 12
    americanfootball = 13
    baseball = 14
    politics = 15
    financial = 16
    greyhound = 17
    volleyball = 18
    handball = 19
    darts = 20
    bandy = 21
    wintersports = 22
    bowls = 24
    pool = 25
    snooker = 26
    tabletennis = 27
    chess = 28
    hockey = 30
    fun = 31
    esports = 32
    inplay = 33
    reserved4 = 34
    mma = 35
    reserved6 = 36
    reserved = 37
    cycling = 38
    reserved9 = 39
    bitcoin = 40
    badminton = 42

class MarketType(Enum):
    moneyline = 0
    over_under = 1
    outright = 2
    game_spread = 3
    set_spread = 4
    correct_score = 5
    future = 6
    basic_prediction = 7
    reserved2 = 8
    reserved3 = 9
    reserved4 = 10
    reserved5 = 11
    reserved6 = 12

class MarketPeriod(Enum):
    undefined = 0
    full_time = 1
    first_set = 2
    second_set = 3
    third_set = 4
    fourth_set = 5
    fifth_set = 6
    first_half = 7
    second_half = 8
    first_quarter = 9
    second_quarter = 10
    third_quarter = 11
    fourth_quarter = 12
    first_period = 13
    second_period = 14
    third_period = 15

class MarketSettlement(Enum):
    binary = 0
    cfd = 1
    cfdi = 2
    exchange = 3

class MarketOrderType(Enum):
    makertaker = 0
    maker = 1
    taker = 2


class MarketCategoryNotFound(Exception):
    pass

class CompNotFound(Exception):
    pass

class MarketStatus(Enum):
    active = 0
    inplay = 1
    suspended = 2
    closed = 3
    settled = 4
    cancelled = 5

class MarketFilter(Schema):
    Cat = EnumField(MarketCategory, load_by=EnumField.NAME, dump_by=EnumField.VALUE, required=True)
    Comp = fields.Str(allow_none=True)
    RunnerAND = fields.List(fields.Str(), allow_none=True)
    TitleAND = fields.List(fields.Str(), allow_none=True)
    TitleNOT = fields.List(fields.Str(), allow_none=True)
    TypeOR = fields.List(EnumField(MarketType, load_by=EnumField.NAME, dump_by=EnumField.VALUE), allow_none=True, missing=None)
    PeriodOR = fields.List(EnumField(MarketPeriod, load_by=EnumField.NAME, dump_by=EnumField.VALUE), allow_none=True, missing=None)
    SettleOR = fields.List(EnumField(MarketSettlement, load_by=EnumField.NAME, dump_by=EnumField.VALUE), allow_none=True, missing=None)
    Descr = fields.Str(allow_none=True)
    ChangedAfter = fields.DateTime(allow_none=True)
    SoftChangedAfter = fields.DateTime(allow_none=True)
    OnlyActive = fields.Bool(missing=True)
    NoZombie = fields.Bool(missing=True)
    FromClosT = fields.DateTime(allow_none=True)
    ToClosT = fields.DateTime(allow_none=True)
    FromID = fields.Integer(allow_none=True, missing=0)
    ToID = fields.Integer(allow_none=True, missing=10000)
    SortPopular = fields.Bool(missing=True)
    MinPop = fields.Float(allow_none=True)
    MaxMargin = fields.Float(allow_none=True)


class RU(Schema):
    Name = fields.Str()
    VisDelay = fields.Integer()
    RedA = fields.Float()
    VolMatched = fields.Float()

class Settler(Schema):
    class Meta:
        unknown = INCLUDE

class ComReceipt(Schema):
    class Meta:
        unknown = INCLUDE

class MarketResult(Schema):
    Comp = fields.Str()
    Descr = fields.Str()
    Title = fields.Str()
    CatID = EnumField(MarketCategory, load_by=EnumField.VALUE, dump_by=EnumField.NAME)
    ClosD = fields.DateTime()
    SettlD = fields.DateTime()
    Status = EnumField(MarketStatus, load_by=EnumField.VALUE, dump_by=EnumField.NAME)
    Ru = fields.List(fields.Nested(RU))
    _Type = EnumField(MarketType, load_by=EnumField.VALUE, dump_by=EnumField.NAME)
    _Period = EnumField(MarketPeriod, load_by=EnumField.VALUE, dump_by=EnumField.NAME)
    SettlT = EnumField(MarketSettlement, load_by=EnumField.VALUE, dump_by=EnumField.NAME)
    Comm = fields.Float()
    Settler = fields.Nested(Settler)
    ComRecip = fields.Nested(ComReceipt)
    MinVal = fields.Float()
    MaxVal = fields.Float()
    LastCh = fields.DateTime()
    LastSoftCh = fields.DateTime()
    LogBugs = fields.Str()
    OrdBStr = fields.Str()
    Pop = fields.Float()
    Margin = fields.Float()
    ID = fields.Integer()


class FairlayPublicAPI(object):

    def __init__(self, base_url='http://185.185.25.238:8080/free'):
        self.base_url = base_url
        self.client = httpx.Client()
        self.marketfilter = MarketFilter()
        self.last_timecheck = arrow.utcnow()

    def _make_request(self, endpoint, payload=None):
        url = self.base_url + str(random.randint(0, 10))
        if payload is not None:
            return self.client.get(f"{url}/{endpoint}/{payload}").json()
        else:
            return self.client.get(f"{url}/{endpoint}")

    def get_markets(self, **kwargs):
        """Get markets
        Keyword arguments:
        Cat = Market Category, can be one of the following:
        ['all', 'soccer', 'tennis', 'golf', 'cricket', 'rugbyunion', 'boxing', 'horseracing', 'Motorsport', 'special', 'rugbyleague', 'basketball', 'americanfootball', 'baseball', 'politics', 'financial', 'greyhound', 'volleyball', 'handball', 'darts', 'bandy', 'wintersports', 'bowls', 'pool', 'snooker', 'tabletennis', 'chess', 'hockey', 'fun', 'esports', 'inplay', 'reserved4', 'mma', 'reserved6', 'reserved', 'cycling', 'reserved9', 'bitcoin', 'badminton']
        Comp = competition, use the get_comps(market_category) method to get a list relevant to the market category in question i.e. FairlayPublicAPI().get_comps('basketball')
        RunnerAND = list of strings which all must be contained in at least one name of one runner of the market
        TitleAND = list of strings which all must appear in the title of the market
        TitleNOT = list of strings which none may appear in the title of the market
        TypeOR = list of strings representing types of market, choices from ['moneyline', 'over_under', 'outright', 'game_spread', 'set_spread', 'correct_score', 'future', 'basic_prediction', 'reserved2', 'reserved3', 'reserved4', 'reserved5', 'reserved6']
        PeriodOR = list of strings representing market periods, choices from ['undefined', 'full_time', 'first_set', 'second_set', 'third_set', 'fourth_set', 'fifth_set', 'first_half', 'second_half', 'first_quarter', 'second_quarter', 'third_quarter', 'fourth_quarter', 'first_period', 'second_period', 'third_period']
        SettleOR = list of strings representing settlement types, choices from ['binary', 'cfd', 'cfdi', 'exchange']
        NoZombie = If True, no empty markets will be returned (without any open order)
        Descr = the given string must appear in the market description
        ChangedAfter = Return markets where the meta data was changed after the given date. Usually the Closing and Settlement Dates of a market is the only data that changes.
        SoftChangedAfter = scrap only the markets where either the meta data or the orderbook has changed since the given date
        FromClosT = Return markets where the closing time is greater than the given one.
        FromID and ToID: Use for paging requests. ToID has a default value of 10000 if not set.
        """
        params = dict(**kwargs)
        params['SoftChangedAfter'] = self.last_timecheck.shift(hours=-2).isoformat()
        self.last_timecheck = arrow.utcnow()
        output = self.marketfilter.load(params)
        mkts = self._make_request('markets', MarketFilter().dumps(output))
        return MarketResult().load(mkts, many=True)

    def get_comps(self, market_category:MarketCategory) -> List:
        return self._make_request('comps', MarketCategory[market_category].value)

    def get_time(self):
        return self._make_request('time')



class FairlayPrivateAPI(object):
    MARKET_CATEGORY = {"Soccer":1,"Tennis":2,"Golf":3,"Cricket":4,"RugbyUnion":5,"Boxing":6,"Horse Racing":7,"Motorsport":8,"Special":10,"Rugby League":11,"Basketball":12,"American Football":13,"Baseball":14,"Politics":15,"Financial":16,"Greyhound":17,"Volleyball":18,"Handball":19,"Darts":20,"Bandy":21,"Winter Sports":22,"Bowls":24,"Pool":25,"Snooker":26,"Table tennis":27,"Chess":28,"Hockey":30,"Fun":31,"eSports":32,"Inplay":33,"reserved4":34,"Mixed Martial Arts":35,"reserved6":36,"reserved":37,"Cycling":38,"reserved9":39,"Bitcoin":40,"Badminton":42}


    MARKET_TYPE = {
            0: 'MONEYLINE', 1: 'OVER_UNDER', 2: 'OUTRIGHT', 3: 'GAMESPREAD', 4: 'SETSPREAD', 5: 'CORRECT_SCORE',
            6: 'FUTURE', 7: 'BASICPREDICTION', 8: 'RESERVED2', 9: 'RESERVED3', 10: 'RESERVED4', 11: 'RESERVED5',
            12: 'RESERVED6'

    }

    MARKET_PERIOD = {
            0: 'UNDEFINED', 1: 'FT', 2: 'FIRST_SET', 3: 'SECOND_SET', 4: 'THIRD_SET', 5: 'FOURTH_SET', 6: 'FIFTH_SET',
            7: 'FIRST_HALF', 8: 'SECOND_HALF', 9: 'FIRST_QUARTER', 10: 'SECOND_QUARTER', 11: 'THIRD_QUARTER',
            12: 'FOURTH_QUARTER', 13: 'FIRST_PERIOD', 14: 'SECOND_PERIOD', 15: 'THIRD_PERIOD',
    }

    MARKET_SETTLEMENT = {
            0: 'BINARY', 1: 'CFD', 2: 'CFDI', 3: 'EXCHANGE'
    }

    MATCHED_ORDER_STATE = {
            0: 'MATCHED', 1: 'RUNNER_WON', 2: 'RUNNER_HALFWON', 3: 'RUNNER_LOST', 4: 'RUNNER_HALFLOST',
            5: 'MAKERVOIDED', 6: 'VOIDED', 7: 'PENDING', 8: 'DECIMAL_RESULT'
    }

    UNMATCHED_ORDER_STATE = {
            0: 'ACTIVE', 1: 'CANCELLED', 2: 'MATCHED', 3: 'MATCHEDANDCANCELLED'
    }

    ORDER_TYPE = {
            0: 'MAKERTAKER', 1: 'MAKER', 2: 'TAKER'
    }

    ENDPOINTS = {
            'get_orderbook': 1, 'get_server_time': 2, 'get_market': 6, 'create_market': 11, 'cancel_all_orders': 16, 'create_account': 20,
            'get_balance': 22, 'get_unmatched_orders': 25, 'get_matched_orders': 27, 'set_absence_cancel_policy': 43,
            'set_force_nonce': 44, 'set_read_only': 49, 'change_orders': 61, 'cancel_orders_on_markets': 83,
            'change_closing': 84, 'settle_market': 86, 'get_public_key': "GETPUBLICKEY", 'get_orderbooks': 4, 'get_markets': 7, 'create_order': 62, 'create_order_with_cancel_time': 13, 'cancel_order': 15, 'cancel_order_with_matches': 75, 'cancel_matched_order': 9, 'confirm_matched_order': 8, 'cancel_orders_on_market': 10, 'change_order': 17, 'change_order_cancel_time': 18, 'get_me': 21, 'get_new_orders': 24, 'bulk_change_orders': 109, 'set_market_maker': 73, 'get_markets_orderbook': 67, 'transfer_funds_withdraw': 81, 'get_user_transactions': 82
    }


    def __init__(self, id, apiaccountid=0, pubkeypem=None, privkeypem=None, server="185.185.25.245", port=18017):
        self.apiaccountid = apiaccountid
        self.id = id
        self.server = server
        self.port = port
        if pubkeypem is not None:
            self.pubkeypem = open(pubkeypem).read()
        if privkeypem is not None:
            self.privkeypem = open(privkeypem).read()
        if pubkeypem is None or privkeypem is None:
            self._generate_keys()
            self.create_account()
            self._dump_config("config.txt")

        self._last_timecheck = arrow.utcnow()
        self._offset = None
        self.serverpubkey = pubkey_xml_to_pem(self._send_request('get_public_key'))
        self.marketfilter = MarketFilter()

    def _generate_keys(self):
        new_key = RSA.generate(2048, e=65537)
        public_key = new_key.publickey().exportKey('PEM')
        private_key = new_key.exportKey('PEM')
        with open("pubkey.pem", "w") as pkf:
            pkf.write(public_key)
        with open("privkey.pem", "w") as privk:
            privk.write(private_key)
        self.pubkeypem = public_key
        self.privkeypem = private_key

    def _sign_message(self, message):
        key = RSA.import_key(self.privkeypem)
        signer = PKCS1_v1_5.new(key)
        digest = SHA512.new(bytes(message, "utf-8"))
        sign = signer.sign(digest)
        return base64.b64encode(sign)

    def _verify_message(self, message):
        if "|" not in message:
            return True
        key = RSA.import_key(self.pubkeypem)
        signer = PKCS1_v1_5.new(key)
        signed_message = message.split("|", 1)[0]
        original_message = message.split("|", 1)[1]
        digest = SHA512.new(original_message)
        if signer.verify(digest, base64.b64decode(signed_message + "=" * ((4 - len(signed_message) % 4) % 4))):
            return True
        else:
            return False

    def _send_request(self, endpoint, data=None):
        nonce = int(round(time.time() * 1000))
        requestid = self.apiaccountid * 1000
        if endpoint != "get_public_key":
            endpoint_code = self.ENDPOINTS[endpoint] + requestid
        else:
            endpoint_code = "GETPUBLICKEY"
        message = "{}|{}|{}".format(nonce, self.id, endpoint_code)
        if data is not None:
            message += "|" + str(data)
        sign = self._sign_message(message)
        wholemessage = "{}|{}<ENDOFDATA>".format(sign.decode("utf-8"), message)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(15)
        s.connect((self.server, self.port))
        s.send(bytes(wholemessage, "utf-8"))
        data = b""
        while True:
            new_data = s.recv(4096)
            if not new_data:
                break
            data += new_data
        s.close()
        output = gzip.decompress(data)
        print(output.decode('utf-8'))
        if output.decode("utf-8").split("|")[-1].startswith("{"):
            return ujson.loads(output.decode("utf-8").split("|")[-1])
        else:
            return output.decode("utf-8").split("|")[-1]


    def _dump_config(self, filename):
        with open(filename, "w") as ft:
            output = ujson.dumps({"public_key": self.pubkeypem, "private_key": self.privkeypem, "apiaccountid": self.apiaccountid, "id": self.id})
            ft.write(output)


    def create_account(self):
        xmlkey = pubkey_pem_to_xml(self.pubkeypem)
        data = xmlkey + "|" + str(self.apiaccountid + 1)
        newme = self._send_request('create_account', data)
        self.apiaccountid += 1
        return newme

    def get_server_time(self):
        return self._send_request('get_server_time')

    def get_me(self):
        return self._send_request('get_me')

    def set_account_read_only(self):
        return self._send_request('set_read_only')

    def get_balance(self):
        return self._send_request('get_balance')

    def get_market(self, market):
        market = self._send_request('get_market', data=market)
        return MarketResult().load(market)

    def get_markets(self, **kwargs):
        params = dict(**kwargs)
        params['SoftChangedAfter'] = self._last_timecheck.shift(hours=-4).isoformat()
        self._last_timecheck = arrow.utcnow()
        output = self.marketfilter.load(params)
        return self._send_request('get_markets', data=MarketFilter().dumps(output))

    def get_markets_orderbook(self, **kwargs):
        params = dict(**kwargs)
        params['SoftChangedAfter'] = self._last_timecheck.shift(hours=-4).isoformat()
        self._last_timecheck = arrow.utcnow()
        output = self.marketfilter.load(params)
        return self._send_request('get_markets_orderbook', data=MarketFilter().dumps(output))

    def get_orderbook(self, market):
        return self._send_request('get_orderbook', data=market)

    def get_orderbooks(self, markets):
        marketcodes = markets
        marketarray = "[" + ",".join(marketcodes) + "]"
        return self._send_request('get_orderbooks', data=marketarray)

    def cancel_all_orders(self):
        return self._send_request('cancel_all_orders')

    def set_force_nonce(self, force_nonce=True):
        return self._send_request('set_force_nonce', str(force_nonce))

    def create_order(self, marketid, runnerid, bidorask, price, amount, type, pending=6000):
        data = f"{marketid}|{runnerid}|{bidorask}|{price}|{amount}|{MarketOrderType[type].value}||{pending}"
        return self._send_request('create_order', data=data)


















