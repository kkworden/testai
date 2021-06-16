'''
This file defines routes related to test case management.
'''

from flask import request, Blueprint
from app.model import db
from app.requests import require_params
from app.responses import success, error
from app.service.case import CaseService

# Use a Flask blueprint to prefix all of our routes.
blueprint = Blueprint('case', __name__, url_prefix='/case')

# Use a service class to abstract database operations
service = CaseService(db.session)


@blueprint.route('/create', methods=['POST'])
@require_params(['test_suite_id'])
def create():
    try:
        new_case = service.create(request.json['test_suite_id'])
        return success({'id': new_case.id})
    except ValueError as e:
        return error(str(e))


@blueprint.route('/edit', methods=['POST'])
@require_params(['case_id'])
def edit():
    try:
        case_id = request.json['case_id']
        kwargs = request.json
        del kwargs['case_id']

        changed = service.edit(case_id, **request.json)
        return success({'changed': changed})
    except ValueError as e:
        return error(str(e))


@blueprint.route('/delete', methods=['POST'])
@require_params(['case_id'])
def delete():
    try:
        deleted = service.delete(request.json['case_id'])
        return success({'deleted': deleted})
    except ValueError as e:
        return error(str(e))
