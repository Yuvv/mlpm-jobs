# -*- coding: utf-8 -*-

# @File   : manger.py
# @Author : Yuvv
# @Date   : 2018/5/4


from flask import Blueprint

from utils.db import PGSession


task_manager_bp = Blueprint('task_manager', __name__)


@task_manager_bp.route('/task/<task_id>', methods=['GET'])
def get_task_info(task_id):
    pass


@task_manager_bp.route('/task/<task_id>/del', methods=['DELETE'])
def del_one_task(task_id):
    pass


@task_manager_bp.route('/tasks/add', methods=['POST'])
def submit_task():
    pass


@task_manager_bp.route('/tasks/list', methods=['GET'])
def list_tasks():
    pass

