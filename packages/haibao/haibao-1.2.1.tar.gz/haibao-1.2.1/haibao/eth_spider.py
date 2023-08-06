# -*- encoding: utf-8 -*-
import os
import sys
import json
from ws4py.client.threadedclient import WebSocketClient


class Client(WebSocketClient):
    def get_target_instId(self, instId):
        return '{"args": [{"instId": "' + instId + '", "channel": "candle15m"}], "op": "subscribe"}'

    def opened(self):
        self.data = {}
        self.target_instIds = ["ETH-USDT", "ADA-USDT", "CFX-USDT"]
        for instId in self.target_instIds:
            self.send(self.get_target_instId(instId))

    def closed(self, code, reason=None):
        pass

    def show(self):
        os.system('cls')
        for k, v in self.data.iteritems():
            print('{}: {}'.format(k, v))

    def received_message(self, resp):
        try:
            resp = json.loads(unicode(resp))
            data, sign = float(resp['data'][0][4]), str(resp['arg']['instId'])
            self.data[sign] = data
            self.show()
        except:
            pass
