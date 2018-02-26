from flask import Blueprint
from flask_restplus import Api

from .person import api as person_api
from .task import api as task_api

api = Api(
    title='Maintenance API',
    version='1.0',
    description='A simple service registry API',
)

blueprint = Blueprint('api', __name__, url_prefix='/v1')

api.init_app(blueprint)

api.add_namespace(person_api)
api.add_namespace(task_api)
