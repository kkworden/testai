from app import TestSuite


class SuiteService:
    '''
    A class to handle all TestSuite operations.
    '''

    def __init__(self, db_session):
        self.db_session = db_session

    def create(self, name):
        '''
        Creates a new test suite.

        Request parameters:
            name: The name of the test suite.

        Returns:
            The new test suite's database object.
        '''
        new_suite = TestSuite(name=name)
        self.db_session.add(new_suite)
        self.db_session.commit()

        self.db_session.refresh(new_suite)

        # Return the created test suite
        return new_suite

    def edit(self, test_suite_id, **kwargs):
        '''
        Updates a test suite's values.

        Request parameters:
            test_suite_id: The id of the test suite to update.
            name: The name of the test suite.
        '''

        suite = self.db_session.get(TestSuite, test_suite_id)
        changed = False

        # Update provided fields
        if 'name' in kwargs:
            suite.name = kwargs['name']
            changed = True

        # Commit to the database
        self.db_session.commit()

        # Return whether or not something changed
        return changed

    def delete(self, test_suite_id):
        '''
        Deletes a test suite.

        Request parameters:
            test_suite_id: The id of the test suite.
        '''
        suite = self.db_session.get(TestSuite, test_suite_id)
        if suite:
            self.db_session.delete(suite)
            self.db_session.commit()

        # Return whether or not something was deleted
        return True if suite else False