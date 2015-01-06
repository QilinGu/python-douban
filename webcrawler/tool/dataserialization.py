# -*- coding: utf-8 -*-
import simplejson as json


class DataSerialization():
    def __init__(self):
        # 初始化
        pass

    def data_to_json(self, data):
        json_data = json.dumps(data)
        return json_data

    def json_to_data(self, json_data):
        data = json.loads(json_data)
        return data