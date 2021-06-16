'''
This file defines routes related to test suite management.
'''

from flask import request, Blueprint
from app.model import db
from app.requests import require_params
from app.responses import success, error
from app.service.suite import SuiteService

# Use a Flask blueprint to prefix all of our routes.
blueprint = Blueprint('suite', __name__, url_prefix='/suite')

# Use a service class to abstract database operations
service = SuiteService(db.session)


@blueprint.route('/create', methods=['POST'])
@require_params(['name'])
def create():
    try:
        new_suite = service.create(request.json['name'])
        return success({'id': new_suite.id})
    except ValueError as e:
        return error(str(e))


@blueprint.route('/edit', methods=['POST'])
@require_params(['suite_id'])
def edit():
    try:
        suite_id = request.json['suite_id']
        kwargs = request.json
        del kwargs['suite_id']

        changed = service.edit(suite_id, **request.json)
        return success({'changed': changed})
    except ValueError as e:
        return error(str(e))


@blueprint.route('/delete', methods=['POST'])
@require_params(['suite_id'])
def delete():
    try:
        deleted = service.delete(request.json['suite_id'])
        return success({'deleted': deleted})
    except ValueError as e:
        return error(str(e))