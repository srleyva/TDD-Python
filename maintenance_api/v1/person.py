from flask_restplus import Namespace, Resource, fields
from .tools import (write_to_table, get_table,
                    delete_from_table, get_item_from_table)


api = Namespace('person', description='Person related queries')

post_model = api.model(
    'Person',
    {
        'name': fields.String(
            required=True,
            description='The person\'s name'),
        'age': fields.Integer(
            required=True,
            description='The person\'s age')
    })

request_model = api.model(
    'Person',
    {
        'id': fields.Integer(
            required=True,
            description='Primary Key'),
        'name': fields.String(
            required=True,
            description='The person\'s name'),
        'age': fields.Integer(
            required=True,
            description='The person\'s age')
    })


@api.route('/')
class Person(Resource):
    @api.doc('list_persons')
    @api.marshal_with(request_model)
    def get(self):
        '''List all persons'''
        table = get_table('person').all()
        return table

    @api.doc('new_person')
    @api.expect(post_model)
    def post(self):
        '''Add a new person'''
        name = write_to_table('person', self.api.payload)
        if not name:
            self.api.abort(
                    409,
                    '{} already exists in the database'.format(
                        self.api.payload.get('name')))
        return {'message': 'Person \'{}\' added.'.format(name)}


@api.route('/<ID>')
@api.param('ID', 'Primary key')
class PersonDetail(Resource):
    def get(self, ID):
        person_record = get_item_from_table('person', ID)
        return person_record

    def delete(self, ID):
        response = delete_from_table('person', ID)
        return response
