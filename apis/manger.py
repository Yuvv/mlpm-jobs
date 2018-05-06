# -*- coding: utf-8 -*-

# @File   : manger.py
# @Author : Yuvv
# @Date   : 2018/5/4

import typing
from json.decoder import JSONDecodeError

from celery.result import AsyncResult
from flask import Blueprint, request, current_app, json
from sqlalchemy import desc

from models import UserTask, MLPMTaskFunc
from tasks.core import MLPMAsyncTask
from utils.db import PGSession
from utils.error import MLPMJobException, MLPMJobErrorEnum
from utils.general import get_param, make_json_resp, import_object

task_manager_bp = Blueprint('task_manager', __name__)


@task_manager_bp.route('/api/v1/task/<task_id>/info', methods=['GET'])
def get_task_info(task_id):
    """
    @api {GET} /api/v1/task/:task_id/info  获取某一个任务的信息
    @apiVersion 1.0.0
    @apiGroup 用户任务
    @apiDescription 根据任务 id 获取某一个任务的信息

    @apiParam (URL Params) {String} task_id 任务 id

    @apiParam (GET Params) {Number} _ 时间戳，utc 时间秒数

    @apiSuccess {String="PENDING","STARTED","RETRY","FAILURE","SUCCESS"} status  任务状态
    @apiSuccess {Object} info  任务返回结果，可能是任意值

    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "code": 0,
        "msg": "OK",
        "data": {
            "status": "SUCCESS",
            "info: {
                "aa": 1,
                "bb": 1,
                "cc": 1,
                "dd": 1
            }
        }
    }
    """
    user_task = PGSession.query(UserTask).filter(UserTask.task_id == task_id).one_or_none()
    if not user_task:
        raise MLPMJobException(MLPMJobErrorEnum.TASK_NOT_FOUND,
                               f'请检查您的任务id="{task_id}"是否正确。')
    result = AsyncResult(task_id)
    r = user_task.as_dict()
    r['status'] = result.status
    return make_json_resp(r)


@task_manager_bp.route('/api/v1/task/<task_id>/result', methods=['GET'])
def get_task_result(task_id):
    """
    @api {GET} /api/v1/task/:task_id/result  查看任务结果
    @apiVersion 1.0.0
    @apiGroup 用户任务
    @apiDescription 根据任务 id 查看任务结果/状态

    @apiParam (URL Params) {String} task_id 任务 id

    @apiParam (GET Params) {Number} _ 时间戳，utc 时间秒数

    @apiSuccess {String} task_id  任务 id
    @apiSuccess {String="PENDING","STARTED","RETRY","FAILURE","SUCCESS"} status  任务状态
    @apiSuccess {Object} result  任务返回结果，可能是任意值
    @apiSuccess {String} traceback  异常调用堆栈

    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "code": 0,
        "msg": "OK",
        "data": {
            "task_id": "e05836d7-75ef-4630-8fdd-1eb0fd4d34b8",
            "status": "SUCCESS",
            "result: {
                "aa": 1,
                "bb": 1,
                "cc": 1,
                "dd": 1
            },
            "traceback": null
        }
    }
    """
    result = AsyncResult(task_id)
    r = dict(task_id=result.id,
             status=result.status,
             result=result.result,
             traceback=result.traceback)
    return make_json_resp(r)


@task_manager_bp.route('/api/v1/task/<task_id>/terminate', methods=['POST'])
def terminate_one_task(task_id):
    """
    @api {GET} /api/v1/task/:task_id/terminate  强制停止某一个任务
    @apiVersion 1.0.0
    @apiGroup 用户任务
    @apiDescription 根据任务 id 强制停止某一个任务。

    @apiParam (URL Params) {String} task_id 任务 id

    @apiParam (GET Params) {Number} _ 时间戳，utc 时间秒数

    @apiSuccess {String="PENDING","STARTED","RETRY","FAILURE","SUCCESS"} status  任务状态
    @apiSuccess {Object} info  任务返回结果，可能是任意值

    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "code": 0,
        "msg": "OK",
        "data": {
            "status": "SUCCESS",
            "info: {
                "aa": 1,
                "bb": 1,
                "cc": 1,
                "dd": 1
            }
        }
    }
    """
    result = AsyncResult(task_id)
    result.revoke(terminate=True)
    return make_json_resp(dict(status=result.status,
                               info=result.info))


@task_manager_bp.route('/api/v1/tasks/submit', methods=['POST'])
def submit_task():
    """
    @api {post} /api/v1/tasks/submit  提交任务
    @apiVersion 1.0.0
    @apiGroup 用户任务
    @apiDescription 提交一个任务

    @apiParam (URL Params) {String} task_id 任务 id

    @apiParam (GET Params) {Number} _ 时间戳，utc 时间秒数

    @apiParam (POST Params) {String} [username] 提交者用户名，非必填，不过不填之后就找不到该用户了
    @apiParam (POST Params) {String} name  函数名，`module:name` 的形式
    @apiParam (POST Params) {String} args  非命名参数，`["a", 1, ["a", 1]]` 的形式，必须可被 json 解析为列表
    @apiParam (POST Params) {String} kwargs 命名参数，`{"a": 1}` 的形式，必须可被 json 解析为 dict
    @apiParam (POST Params) {String} [desc]  任务描述信息

    @apiSuccess {Number} id  用户任务 id，没什么用
    @apiSuccess {Number} func_id  对应函数的 id，没什么用
    @apiSuccess {String} username  用户名
    @apiSuccess {String} args  非命名参数
    @apiSuccess {String} kwargs  命名参数
    @apiSuccess {String} desc  描述信息
    @apiSuccess {String} task_id  任务 id，真正有用的 id 是这个
    @apiSuccess {String} create_date  任务创建时间，`%a, %d %b %Y %H:%M:%S GMT`

    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "code": 0,
        "msg": "OK",
        "data": {
            "args": "[\"aa bb cc dd\"]",
            "create_date": "Sat, 05 May 2018 08:25:32 GMT",
            "desc": null,
            "func_id": 1,
            "id": 1,
            "kwargs": "{}",
            "task_id": "325a0a70-abe5-4908-b3e3-f77266306a05",
            "username": "yuvv"
        }
    }
    """
    username = get_param(request.form, 'username', required=False)
    func_name = get_param(request.form, 'name')
    func_args = get_param(request.form, 'args')
    func_kwargs = get_param(request.form, 'kwargs')
    func_desc = get_param(request.form, 'desc', required=False)

    func_id = PGSession.query(MLPMTaskFunc.id).filter(MLPMTaskFunc.name == func_name).scalar()
    if not func_id:
        raise MLPMJobException(MLPMJobErrorEnum.FUNC_NOT_FOUND)

    args = json.loads(func_args)
    if not isinstance(args, typing.Iterable):
        raise MLPMJobException(MLPMJobErrorEnum.BAD_FUNC_PARAM,
                               '`args` 必须是合法的可迭代对象。')

    kwargs = json.loads(func_kwargs)
    if not isinstance(kwargs, typing.Dict):
        raise MLPMJobException(MLPMJobErrorEnum.BAD_FUNC_PARAM,
                               '`kwargs` 必须是合法的字典对象。')

    func = import_object(func_name)
    if not isinstance(func, MLPMAsyncTask):
        raise MLPMJobException(MLPMJobErrorEnum.ILLEGAL_FUNC,
                               '你选择的函数不是合法的 MLPM 异步函数')

    session = PGSession()
    try:
        r = func.delay(*args, **kwargs)

        user_task = UserTask(username=username, func_id=func_id,
                             task_id=r.id, args=func_args, kwargs=func_kwargs,
                             desc=func_desc)
        session.add(user_task)
        session.commit()
        return make_json_resp(user_task.as_dict())
    except JSONDecodeError:
        current_app.logger.warning(f'<User: {username}> submit a task with bad arguments: ({func_args}, {func_kwargs})')
        raise MLPMJobException(MLPMJobErrorEnum.BAD_ARGUMENTS,
                               '您提供的函数参数不是可解析的 JSON 字符串！')
    except Exception:
        current_app.logger.exception('Unknown error occurs:')
        session.rollback()
        raise MLPMJobException(MLPMJobErrorEnum.UNKNOWN_ERROR)
    finally:
        session.close()


@task_manager_bp.route('/api/v1/tasks/list', methods=['GET'])
def list_tasks():
    """
    @api {GET} /api/v1/tasks/list  查看任务列表
    @apiVersion 1.0.0
    @apiGroup 用户任务
    @apiDescription 查看某一格用户的任务列表

    @apiParam (URL Params) {String} task_id 任务 id

    @apiParam (GET Params) {Number} _ 时间戳，utc 时间秒数
    @apiParam (GET Params) {String} username 提交者用户名，非必填，不过不填之后就找不到该用户了
    @apiParam (GET params) {Number} [page=1] 需要获取的页数，可选，默认第一页
    @apiParam (GET params) {Number} [per_page=10] 每一页的数量，可选，默认 10

    @apiSuccess {Number} id  user_task id，没什么用
    @apiSuccess {Number} func_id  对应函数的 id，没什么用
    @apiSuccess {String} username  用户名
    @apiSuccess {String} args  非命名参数
    @apiSuccess {String} kwargs  命名参数
    @apiSuccess {String} desc  描述信息
    @apiSuccess {String="PENDING","STARTED","RETRY","FAILURE","SUCCESS"} status  任务状态
    @apiSuccess {String} task_id  任务 id，真正有用的 id 是这个
    @apiSuccess {String} create_date  任务创建时间，`%a, %d %b %Y %H:%M:%S GMT`

    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "code": 0,
        "msg": "OK",
        "data": {
            "args": "[\"aa bb cc dd\"]",
            "create_date": "Sat, 05 May 2018 08:25:32 GMT",
            "desc": null,
            "func_id": 1,
            "id": 1,
            "kwargs": "{}",
            "task_id": "325a0a70-abe5-4908-b3e3-f77266306a05",
            "username": "yuvv"
        }
    }
    """
    username = get_param(request.args, 'username', required=True)
    page = max(1, get_param(request.args, 'page', convert_to=int) or 1)
    per_page = max(1, get_param(request.args, 'per_page', convert_to=int) or 10)

    q = PGSession.query(UserTask).filter(UserTask.username == username).order_by(desc(UserTask.create_date))
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    qs = q.slice(start_idx, end_idx)
    rs = []
    for user_task in qs:
        r = user_task.as_dict()
        result = AsyncResult(user_task.task_id)
        r['status'] = result.status
        rs.append(r)

    return make_json_resp(rs)


@task_manager_bp.route('/api/v1/task_funcs/list', methods=['GET'])
def list_mlpm_task_funcs():
    """
    @api {GET} /api/v1/task_funcs/list  查看任务函数列表
    @apiVersion 1.0.0
    @apiGroup 任务函数
    @apiDescription 列出已存在的任务函数

    @apiParam (URL Params) {String} task_id 任务 id

    @apiParam (GET Params) {Number} _ 时间戳，utc 时间秒数
    @apiParam (GET params) {Number} [page=1] 需要获取的页数，可选，默认第一页
    @apiParam (GET params) {Number} [per_page=10] 每一页的数量，可选，默认 10

    @apiSuccess {Number} id  user_task id，没什么用
    @apiSuccess {Number} func_id  对应函数的 id，没什么用
    @apiSuccess {String} username  用户名
    @apiSuccess {String} args  非命名参数
    @apiSuccess {String} kwargs  命名参数
    @apiSuccess {String} desc  描述信息
    @apiSuccess {String="PENDING","STARTED","RETRY","FAILURE","SUCCESS"} status  任务状态
    @apiSuccess {String} task_id  任务 id，真正有用的 id 是这个
    @apiSuccess {String} create_date  任务创建时间，`%a, %d %b %Y %H:%M:%S GMT`

    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "code": 0,
        "msg": "OK",
        "data": {
            "args": "[\"aa bb cc dd\"]",
            "create_date": "Sat, 05 May 2018 08:25:32 GMT",
            "desc": null,
            "func_id": 1,
            "id": 1,
            "kwargs": "{}",
            "task_id": "325a0a70-abe5-4908-b3e3-f77266306a05",
            "username": "yuvv"
        }
    }
    """
    page = max(1, get_param(request.args, 'page', convert_to=int) or 1)
    per_page = max(1, get_param(request.args, 'per_page', convert_to=int) or 10)

    q = PGSession.query(MLPMTaskFunc).order_by(desc(MLPMTaskFunc.pub_date))
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    qs = q.slice(start_idx, end_idx)
    rs = []
    for func in qs:
        rs.append(func.as_dict())

    return make_json_resp(rs)
