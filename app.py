import logging.config
from flask import Flask, request
from werkzeug.exceptions import MethodNotAllowed, NotFound, InternalServerError

from apis import task_manager_bp
from utils.error import MLPMJobErrorEnum, MLPMJobException, default_err_handler
from utils.db import PGSession
from utils.middleware import check_authorization
from utils.general import get_param
import settings


def create_app():
    logging.config.dictConfig(settings.LOGGING)

    app = Flask(__name__)

    # register blueprint
    app.register_blueprint(task_manager_bp)

    # configurations
    # app.config.from_object('settings')
    app.config['debug'] = settings.DEBUG

    # exception handler
    app.register_error_handler(MLPMJobException, default_err_handler)
    app.register_error_handler(MethodNotAllowed,
                               lambda ex: default_err_handler(
                                   MLPMJobException(MLPMJobErrorEnum.METHOD_NOT_ALLOWED)))
    app.register_error_handler(NotFound,
                               lambda ex: default_err_handler(MLPMJobException(MLPMJobErrorEnum.NOT_FOUND)))
    app.register_error_handler(InternalServerError,
                               lambda ex: default_err_handler(MLPMJobException(MLPMJobErrorEnum.UNKNOWN_ERROR)))

    @app.before_request
    def require_authorization():
        _ = get_param(request.args, '_', required=True, convert_to=float)
        auth = request.headers.get('Authorization')
        if not settings.DEBUG:
            check_authorization(_, auth)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        PGSession.remove()

    return app


if __name__ == '__main__':
    mlpm_jobs_app = create_app()
    # WARNING: 这种方式切哦对那个会导致 celery 失效，原因不明
    mlpm_jobs_app.run(debug=settings.DEBUG)
