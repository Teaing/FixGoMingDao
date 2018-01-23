# encoding: utf-8

import json
from urlparse import urlparse
from config import address_info

"""You can write youself control code in here..."""


def mingdao_proxy_request_handle(flow):
    """MingDao send data to server before processing"""
    flow.request.anticache()  # disable cache
    flow.request.anticomp()  # disable gzip compress
    mingdaoPatch(flow, False)

    # print flow.request.headers
    # print flow.request.headers['Host']

    # change the request headers['Host']
    # flow.request.headers['X-Online-Host'] = 'wap.gd.10086.cn'


def mingdao_proxy_response_handle(flow):
    """MingDao request task is over"""
    mingdaoPatch(flow)
    # print flow.request
    # print flow.request.path
    # print flow.request.method
    # print flow.response.body
    # if flow.request.method == 'POST':
    # print flow.response.body


def mingdaoPatch(flow, after=True):
    url = urlparse(
        flow.request.url)  # ParseResult(scheme='http', netloc='www.love.com', path='/', params='', query='a=1&b=2', fragment='')
    if (url.netloc == 'check.mingdao.com'):
        if after:
            if '/MyAttendance/AttendanceConfig' == flow.request.path:
                sourceData = flow.response.body
                sourceData = json.loads(
                    sourceData.replace('\'', '\"').replace('None,', '\"None\",').replace('False,',
                                                                                         '\"False\",').replace(
                        'True,', '\"True\",').replace('u\"', '\"'))
                sourceData['addressModes'][0]['punchCardRange'] = 200000
                flow.response.body = json.dumps(sourceData).replace('\"true\",', 'True,').replace('\"false\",',
                                                                                                  'False,').replace(
                    '\"None\",', 'None,')
        else:
            if 'POST' == flow.request.method and '/MyAttendance' == flow.request.path:
                json_data = flow.request.body
                json_data = json.loads(json_data)
                json_data[
                    'locationAddress'] = address_info[0]
                json_data['longitude'] = float(address_info[1])
                json_data['latitude'] = float(address_info[2])
                flow.request.body = json.dumps(json_data)
