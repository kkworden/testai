from unittest import mock
import unittest

import pytest

from app.model import Step
from app.service.step import StepService

TEST_STEP_ID = 'step_id'
TEST_CASE_ID = 'case_id'
TEST_CONTENTS = 'contents'
TEST_TYPE = 'action'


class TestStepService(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _setup_service(self):
        self.db_session = mock.MagicMock()
        self.service = StepService(self.db_session)

    def test_create(self):
        self.service.create(TEST_CASE_ID, TEST_CONTENTS, TEST_TYPE)

        # Check that the database is called
        assert self.db_session.add.called
        assert self.db_session.commit.called
        assert self.db_session.refresh.called

    def test_create_bad_type(self):
        # Test when we call create with a bad type
        expected_exception = None
        try:
            self.service.create(TEST_CASE_ID, TEST_CONTENTS, 'jibberish')
        except ValueError as e:
            expected_exception = e

        # Check that an exception was thrown
        assert expected_exception is not None

    def test_edit(self):
        kwargs = {'test_case_id': TEST_CASE_ID, 'contents': TEST_CONTENTS, 'step_type': TEST_TYPE}
        self.service.edit(TEST_STEP_ID, **kwargs)

        # Check that the database is called
        self.db_session.get.assert_called_once_with(Step, TEST_STEP_ID)
        assert self.db_session.commit.called

    def test_edit_bad_type(self):
        # Test when we call edit with a bad type
        expected_exception = None
        try:
            kwargs = {'step_type': 'jibberish'}
            self.service.edit(TEST_STEP_ID, **kwargs)
        except ValueError as e:
            expected_exception = e

        # Check that an exception was thrown
        assert expected_exception is not None

    def test_delete(self):
        self.service.delete(TEST_STEP_ID)

        # Check that the database is called
        self.db_session.get.assert_called_once_with(Step, TEST_STEP_ID)
        assert self.db_session.delete.called
        assert self.db_session.commit.called
