'''
This file defines our database model.
'''

from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

from sqlalchemy.orm import backref

db = SQLAlchemy()


@dataclass
class TestSuite(db.Model):
    '''
    Defines a test suite. A test suite is a collection of test cases.
    '''

    __tablename__ = 'testsuite'
    __test__ = False  # Prevent PyTest from picking up this class

    id = db.Column(db.Integer, primary_key=True)

    # Suite name is limited to 128 characters to prevent boundless data storage.
    name = db.Column(db.Unicode(length=128), nullable=False)

    # The test suite's cases (one-to-many)
    test_cases = db.relationship('TestCase', backref=backref('test_suite', cascade='all,delete'), lazy='dynamic')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'test_cases': [test_case.to_json() for test_case in self.test_cases]
        }


@dataclass
class TestCase(db.Model):
    '''
    Defines a test case. A test case is a collection of actions and assertions.
    '''

    __tablename__ = 'testcase'
    __test__ = False  # Prevent PyTest from picking up this class

    id = db.Column(db.Integer, primary_key=True)

    # Establish a relationship with the TestSuite model. Many cases can exist in a single test suite.
    test_suite_id = db.Column(db.Integer(), db.ForeignKey('testsuite.id', ondelete='CASCADE'))

    # The test case's steps (one-to-many)
    steps = db.relationship('Step', backref=backref('test_case', cascade='all,delete'), lazy='dynamic')

    def to_json(self):
        return {
            'id': self.id,
            'test_suite_id': self.test_suite_id,
            'steps': [step.to_json() for step in self.steps]
        }


@dataclass
class Step(db.Model):
    '''
    Defines a test step. Defines what type of step (action, assertion) it is, and the test
    case that this step is associated with, along with ordering.
    '''

    __tablename__ = 'step'

    id = db.Column(db.Integer, primary_key=True)

    # Establish a relationship with the TestCase model. Many steps can exist in a single test case.
    test_case_id = db.Column(db.Integer(), db.ForeignKey('testcase.id', ondelete='CASCADE'))

    # Contents of a step is limited to 1024 characters to prevent boundless data storage.
    contents = db.Column(db.Unicode(length=1024), nullable=False)

    # Will be either 'assertion' or 'action'. Limited to 9 characters as 'assertion' is the max length.
    type = db.Column(db.Unicode(length=9), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'test_case_id': self.test_case_id,
            'contents': self.contents,
            'type': self.type
        }