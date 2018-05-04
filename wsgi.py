# -*- coding: utf-8 -*-

# @File   : wsgi.py
# @Author : Yuvv
# @Date   : 2018/5/4


from app import create_app

mlpm_jobs_app = create_app()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server('localhost', 5000, mlpm_jobs_app)
    httpd.serve_forever()
