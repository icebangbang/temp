# coding=utf-8
from flask import make_response
import json


def response_to(data=None, message=None, success=True, cls=None, **kwargs):
    # type: (object, object, object, object, object) -> object
    """ 封装 json 响应"""
    result = kwargs
    result['success'] = success
    result['message'] = message
    result['data'] = data

    # # 如果提供了 data，那么不理任何其他参数，直接响应 data
    # if not data:
    #     # data = kwargs
    #     result['error'] = error
    #     if message:
    #         # 除非显示提供 error 的值，否则默认为 True
    #         # 意思是提供了 message 就代表有 error
    #         result['message'] = message
    #         if error is None:
    #             result['error'] = True
    #     else:
    #         # 除非显示提供 error 的值，否则默认为 False
    #         # 意思是没有提供 message 就代表没有 error
    #         if error is None:
    #             data['error'] = False
    # # if not isinstance(data, dict):
    # #     data = {'error':True, 'message':'data 必须是一个 dict！'}
    resp = make_response(json.dumps(result, cls=cls))
    # 跨域设置
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    resp.headers["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT"
    resp.headers[
        "Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept, Connection, User-Agent, Cookie,Cache-Control"
    return resp


a = 'i like ,it,just'
print a.find('it2')