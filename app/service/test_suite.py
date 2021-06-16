from unittest import mock
import unittest

import pytest

from app.model import TestSuite
from app.service.suite import SuiteService

TEST_SUITE_ID = 'suite_id'
TEST_NAME = 'name'


class TestSuiteService(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _setup_service(self):
        self.db_session = mock.MagicMock()
        self.service = SuiteService(self.db_session)

    def test_create(self):
        self.service.create(TEST_SUITE_ID)

        # Check that the database is called
        assert self.db_session.add.called
        assert self.db_session.commit.called
        assert self.db_session.refresh.called

    def test_edit(self):
        kwargs = {'name': TEST_NAME}
        self.service.edit(TEST_SUITE_ID, **kwargs)

        # Check that the database is called
        self.db_session.get.assert_called_once_with(TestSuite, TEST_SUITE_ID)
        assert self.db_session.commit.called

    def test_delete(self):
        self.service.delete(TEST_SUITE_ID)

        # Check that the database is called
        self.db_session.get.assert_called_once_with(TestSuite, TEST_SUITE_ID)
        assert self.db_session.delete.called
        assert self.db_session.commit.called
