from flask_restplus import Namespace, Resource, fields
from .tools import (write_to_table, get_table,
                    delete_from_table, get_item_from_table)


api = Namespace('task', description='Task related queries')

put_model = api.model(
    'Task',
    {
        'name': fields.String(
            required=True,
            description='The task\'s name')
    })

request_model = api.model(
    'Task',
    {
        'id': fields.Integer(
            required=True,
            description='Primary Key'),
        'name': fields.String(
            required=True,
            description='The task\'s name')
    })


@api.route('/')
class Task(Resource):
    @api.doc('list_tasks')
    @api.marshal_with(request_model)
    def get(self):
        '''List all tasks'''
        table = get_table('task')
        return table.all()

    @api.doc('new_task')
    @api.expect(put_model)
    def post(self):
        '''Add a new task'''
        name = write_to_table('task', self.api.payload)
        if not name:
            self.api.abort(
                    409,
                    '{} already exists in the database'.format(
                        self.api.payload.get('name')))
        return {'message': 'Task \'{}\' added.'.format(name)}


@api.route('/<ID>')
@api.param('ID', 'Primary key')
class TaskDetail(Resource):
    def get(self, ID):
        task_record = get_item_from_table('task', ID)
        return task_record

    def delete(self, ID):
        response = delete_from_table('task', ID)
        return response
