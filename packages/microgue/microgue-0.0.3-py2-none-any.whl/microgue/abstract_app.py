import json
import logging
import traceback
from .constants.error_constants import ErrorConstants
from flask import Flask, request, Response, g
from .security.generic import is_allowed_by_all
from werkzeug.exceptions import NotFound, MethodNotAllowed

logging.basicConfig()
logger = logging.getLogger('microgue')
logger.setLevel(logging.DEBUG)


class AbstractApp:
    views = []
    blueprints = []
    mask_request_headers_fields = []
    mask_request_data_fields = []

    def __init__(self):
        self.app = Flask(__name__)
        self.app.url_map.strict_slashes = False
        self.register_index()
        self.register_views()
        self.register_blueprints()
        self.register_before_request_handler()
        self.register_after_request_handler()
        self.register_error_handlers()

    def register_index(self):
        @self.app.route("/", methods=['GET'])
        @is_allowed_by_all
        def index():
            return Response(json.dumps({'message': 'success'}), status=200)

    def register_views(self):
        for view in self.views:
            view.register(self.app)

    def register_blueprints(self):
        for blueprint in self.blueprints:
            self.app.register_blueprint(blueprint)

    def register_before_request_handler(self):
        self.app.before_request(self.before_request_handler)

    @staticmethod
    def before_request_handler():
        # mask request header fields
        try:
            request_headers = {}
            for key, value in request.headers:
                if key in self.mask_request_headers_fields:
                    request_headers[key] = '*****'
                else:
                    request_headers[key] = value
        except:
            request_headers = {}

        # mask request data fields
        try:
            request_data = json.loads(request.data.decode('utf-8'))
            for mask_request_data_field in self.mask_request_data_fields:
                if mask_request_data_field in request_data:
                    request_data[mask_request_data_field] = '*****'
        except:
            request_data = {}

        logger.debug('########## Request Received ########################################')
        logger.debug({'method': request.method})
        logger.debug({'url': request.url})
        logger.debug({'headers': request_headers})
        logger.debug({'body': request_data})

    def register_after_request_handler(self):
        self.app.after_request(self.after_request_handler)

    @staticmethod
    def after_request_handler(response):
        if not g.get('authenticated') and int(response.status_code) < 400:
            response = Response(json.dumps({'error': ErrorConstants.App.UNABLE_TO_AUTHENTICATE}), status=401)

        response.headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,X-Api-Key,X-Amz-Security-Token,Authorization,session_id"
        }

        logger.debug('########## Response Sent ########################################')
        logger.debug({'status': response.status})
        logger.debug({'headers': response.headers})
        logger.debug({'body': response.response})

        return response

    def register_error_handlers(self):
        self.app.register_error_handler(NotFound, self.not_found_error)
        self.app.register_error_handler(MethodNotAllowed, self.method_not_allowed_error)
        self.app.register_error_handler(Exception, self.internal_server_error)

    @staticmethod
    def not_found_error(e):
        logger.debug('########## Not Found Error ########################################')
        logger.debug("{}: {}".format(e.__class__.__name__, e))
        logger.debug(traceback.format_exc())
        return Response(json.dumps({'error': ErrorConstants.App.REQUESTED_URL_NOT_FOUND}), status=404)

    @staticmethod
    def method_not_allowed_error(e):
        logger.debug('########## Method Not Allowed Error ########################################')
        logger.debug("{}: {}".format(e.__class__.__name__, e))
        logger.debug(traceback.format_exc())
        return Response(json.dumps({'error': ErrorConstants.App.METHOD_NOT_ALLOWED}), status=405)

    @staticmethod
    def internal_server_error(e):
        logger.critical('########## Internal Server Error ########################################')
        logger.critical("{}: {}".format(e.__class__.__name__, e))
        logger.critical(traceback.format_exc())
        return Response(json.dumps({'error': ErrorConstants.App.INTERNAL_SERVER_ERROR}), status=500)
