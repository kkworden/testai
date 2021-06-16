'''
This file defines routes related to test case management.
'''

from flask import request, Blueprint

from app.model import db
from app.requests import require_params
from app.responses import success, error
from app.service.step import StepService

# Use a Flask blueprint to prefix all of our routes.
blueprint = Blueprint('step', __name__, url_prefix='/step')

# Use a service class to abstract database operations
service = StepService(db.session)


@blueprint.route('/create', methods=['POST'])
@require_params(['test_case_id', 'contents', 'step_type'])
def create():
    try:
        new_step = service.create(request.json['test_case_id'], request.json['contents'], request.json['step_type'])
        return success({'id': new_step.id})
    except ValueError as e:
        return error(str(e))


@blueprint.route('/edit', methods=['POST'])
@require_params(['step_id'])
def edit():
    try:
        step_id = request.json['step_id']
        kwargs = request.json
        del kwargs['step_id']

        changed = service.edit(step_id, **request.json)
        return success({'changed': changed})
    except ValueError as e:
        return error(str(e))


@blueprint.route('/delete', methods=['POST'])
@require_params(['step_id'])
def delete():
    try:
        deleted = service.delete(request.json['step_id'])
        return success({'deleted': deleted})
    except ValueError as e:
        return error(str(e))

