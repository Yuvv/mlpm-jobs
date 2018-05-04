# -*- coding: utf-8 -*-

# @File   : handler.py
# @Author : Yuvv
# @Date   : 2018/5/4


from flask import json, Response


def default_err_handler(ex):
    resp = Response(json.dumps(ex.to_dict(), ensure_ascii=False),
                    status=ex.status,
                    content_type='application/json; charset=utf-8')
    return resp
