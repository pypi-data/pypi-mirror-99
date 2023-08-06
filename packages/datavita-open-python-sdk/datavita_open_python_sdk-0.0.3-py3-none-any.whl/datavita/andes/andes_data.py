#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-02-02 17:38
    @Author : haifeng
    @Version：V 0.1
    @File : andes_data.py
    @desc :
"""
import datetime
import hashlib
import json
import random
import time
import typing
import pandas as pd

from datavita.andes.andes_apis import andes_apis_dict
from datavita.core.auth import Auth
from datavita.core.common import contants
from datavita.core.transport.comrequests import CommonRequests
from datavita.core.transport.http import Request
from datavita.core.utils import log
from datavita.core.utils.middleware import Middleware


def tid_mak():
    uuid_str = '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join(
        [str(random.randint(1, 10)) for i in range(5)])
    return uuid_str


class AndesData:
    """
        中台数据
        初始化固定参数 auth 超时 最大重试次数
    """

    def __init__(
            self,
            auth: typing.Optional[Auth] = None,
            base_url: str = contants.BASE_URL,
            timeout: int = contants.SESSION_PERIOD_TIMEOUT,
            max_retries: int = contants.MAX_RETRIES,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.auth = auth
        middleware = Middleware()
        self._middleware = middleware
        self.logger = log.default_logger

    def _send(self, api_name, action, api, params, max_retries, timeout):
        try:
            req = self._build_http_request(api_name, action, api, params=params)
            resp = CommonRequests(auth=self.auth, max_retries=max_retries, timeout=timeout).send(req=req)
        except Exception as e:
            return pd.DataFrame()
            raise e
        return self._middleware.logged_response_df_handler(self.auth, resp, resp.request.request_name)

    def _build_http_request(self, api_name, action, api, params) -> Request:
        nonce = tid_mak()
        timestamp = int(time.time())
        date_str = datetime.datetime.now()
        path_parm = api.replace(contants.BASE_URL, '')
        parm_md5 = hashlib.md5(str(json.dumps(params, ensure_ascii=False)).encode(encoding='UTF-8')).hexdigest()
        if action.upper() == 'GET':
            sign_str = f"""{action.upper()}\n*/*\n\n\n{date_str}\nx-datavita-nonce:{nonce}\nx-datavita-signature-method:HmacSHA1\n{path_parm}"""
        else:
            sign_str = f"""{action.upper()}\n*/*\n{parm_md5}\napplication/json\n{date_str}\nx-datavita-nonce:{nonce}\nx-datavita-signature-method:HmacSHA1\n{path_parm}"""
        signature = self.auth.make_authorization(sign_str)
        if action.upper() == 'GET':
            headers = {
                'Accept': '*/*',
                'x-datavita-key': '{}'.format(self.auth.access_id),
                'x-datavita-nonce': '{}'.format(nonce),
                'x-datavita-timestamp': '{}'.format(timestamp),
                'x-datavita-signature-method': 'HmacSHA1',
                'date': '{}'.format(date_str),
                'x-datavita-signature-headers': 'x-datavita-signature-method,x-datavita-nonce',
                'x-datavita-signature': '{}'.format(signature)
            }
        else:
            headers = {
                'Accept': '*/*',
                'Content-Type': 'application/json',
                'x-datavita-key': '{}'.format(self.auth.access_id),
                'x-datavita-nonce': '{}'.format(nonce),
                'x-datavita-timestamp': '{}'.format(timestamp),
                'x-datavita-signature-method': 'HmacSHA1',
                'date': '{}'.format(date_str),
                'x-datavita-signature-headers': 'x-datavita-signature-method,x-datavita-nonce',
                'x-datavita-signature': '{}'.format(signature)
            }
        return Request(
            request_name=api_name,
            url=api,
            method=action.upper(),
            data=params,
            headers=headers
        )

    def ind_data_list(self, ind_code):
        """
           根据行业代码获取该行业下的数据指标
        :param ind_code: 行业code
        :return:
        """
        params = ind_code
        url = andes_apis_dict.get("ind_data_list").format(base_url=self.base_url)
        df = self._send(api_name="根据行业代码获取该行业下的数据指标", action='post', api=url, params=params,
                        max_retries=self.max_retries,
                        timeout=self.timeout)
        df.rename(columns={'dataCode': 'data_code', 'dataName': 'data_name', 'unit': 'tsd_unit', 'freq': 'tsd_freq',
                           'source': 'tsd_source'}, inplace=True)
        return df

    def data_info(self, data_code, start_day=19000101, end_day=21001231):
        """
           根据指标数据data_code获取数据
        :param end_day: 结束时间
        :param start_day: 开始时间
        :param data_code: 数据code
        :return:
        """
        params = {
            'dataCode': data_code,
            'startDay': start_day,
            'endDay': end_day
        }
        url = andes_apis_dict.get("data_info").format(base_url=self.base_url)
        df = self._send(api_name="根据指标数据data_code获取数据", action='post', api=url, params=params,
                        max_retries=self.max_retries,
                        timeout=self.timeout)
        df.rename(
            columns={'hc_ts_data_code': 'data_code', 'hc_ts_data_name': 'data_name', 'hc_ts_data_value': 'data_value',
                     'hc_ts_data_day': 'data_day'}, inplace=True)
        return df
