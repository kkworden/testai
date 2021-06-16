from unittest import mock
import unittest

import pytest

from app.model import TestCase, TestSuite
from app.service.case import CaseService

TEST_CASE_ID = 'case_id'
TEST_SUITE_ID = 'suite_id'


class TestCaseService(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _setup_service(self):
        self.db_session = mock.MagicMock()
        self.service = CaseService(self.db_session)

    def test_create(self):
        self.service.create(TEST_SUITE_ID)

        # Check that the database is called
        self.db_session.get.assert_called_once_with(TestSuite, TEST_SUITE_ID)
        assert self.db_session.add.called
        assert self.db_session.commit.called
        assert self.db_session.refresh.called

    def test_create_suite_nonexistent(self):
        # Mock when the database can't find our TestSuite
        self.db_session.get = lambda _, __: None

        expected_exception = None
        try:
            self.service.create(TEST_SUITE_ID)
        except ValueError as e:
            expected_exception = e

        # Check that an exception was thrown
        assert expected_exception is not None

    def test_edit(self):
        kwargs = {'test_suite_id': TEST_SUITE_ID}
        self.service.edit(TEST_CASE_ID, **kwargs)

        # Check that the database is called
        self.db_session.get.assert_has_calls([mock.call(TestCase, TEST_CASE_ID), mock.call(TestSuite, TEST_SUITE_ID)])
        assert self.db_session.commit.called

    def test_delete(self):
        self.service.delete(TEST_CASE_ID)

        # Check that the database is called
        self.db_session.get.assert_called_once_with(TestCase, TEST_CASE_ID)
        assert self.db_session.delete.called
        assert self.db_session.commit.called
