import os
import json
from flask import Flask, jsonify

from .model import db, TestSuite
from .responses import success

from app.route.case import blueprint as case_blueprint
from app.route.suite import blueprint as suite_blueprint
from app.route.step import blueprint as step_blueprint


def create_app():
    '''
    Creates the Flask app.
    '''
    app = Flask(__name__, instance_relative_config=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.environ.get('TEST_DATABASE_DIR'), 'test.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database model
    db.init_app(app)

    # Create our DB tables
    with app.app_context():
        db.create_all()

    # Mount routes
    mount_routes(app)

    return app


def mount_routes(app):
    '''
    Mounts all routes. Routes are defined as blueprints to define route prefixes more easily.
    '''
    app.register_blueprint(case_blueprint)
    app.register_blueprint(suite_blueprint)
    app.register_blueprint(step_blueprint)

    @app.route('/')
    def index():
        '''
        Index view. Dumps the database.
        '''
        result = [suite.to_json() for suite in TestSuite.query.all()]
        return jsonify(result=result), 200, {'Content-Type': 'application/json'}
