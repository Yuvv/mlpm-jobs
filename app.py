import logging.config
from flask import Flask, request, g
from werkzeug.exceptions import MethodNotAllowed, NotFound, InternalServerError

from apis import task_manager_bp
from utils.error import MLPMJobErrorEnum, MLPMJobException, default_err_handler
from utils.db import PGSession
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
        g.user_info = None
        _params = request.args if request.method == 'GET' else request.form
        token = _params.get('token', '')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        PGSession.remove()

    return app


if __name__ == '__main__':
    mlpm_jobs_app = create_app()
    mlpm_jobs_app.run()
