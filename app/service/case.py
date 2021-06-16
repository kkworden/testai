from app.model import TestCase, TestSuite


class CaseService:
    '''
    A class to handle all TestCase operations.
    '''

    def __init__(self, db_session):
        self.db_session = db_session

    def create(self, test_suite_id):
        '''
        Creates a test case.

        Request parameters:
            test_suite_id: The TestSuite to attach this test case to.

        Returns:
            The new test case's database object.
        '''
        # Check if the test suite the user wants to attach this case to is valid.
        suite = self.db_session.get(TestSuite, test_suite_id)
        if not suite:
            raise ValueError('Not a valid test suite.')

        new_case = TestCase(test_suite_id=test_suite_id)

        # Commit to the database
        self.db_session.add(new_case)
        self.db_session.commit()

        self.db_session.refresh(new_case)

        # Return the new case
        return new_case

    def edit(self, case_id, **kwargs):
        '''
        Updates a test case's values.

        Request parameters:
            case_id: The id of the case to update.
            test_suite_id: The id of the test suite to attach this case to.

        Returns:
            True if the record was updated, otherwise False.
        '''
        case = self.db_session.get(TestCase, case_id)
        changed = False

        # Update provided fields
        if 'test_suite_id' in kwargs:
            # Check if the test suite the user wants to attach this case to is valid.
            suite = self.db_session.get(TestSuite, kwargs['test_suite_id'])
            if not suite:
                raise ValueError('Not a valid test suite.')

            case.test_suite_id = kwargs['test_suite_id']
            changed = True

        # Commit to the database
        self.db_session.commit()

        # Return whether or not something changed
        return changed

    def delete(self, case_id):
        '''
        Deletes a test case.

        Request parameters:
            case_id: The id of the test case.

        Returns:
            True if the record was deleted, otherwise False.
        '''
        case = self.db_session.get(TestCase, case_id)
        if case:
            self.db_session.delete(case)
            self.db_session.commit()

        # Return whether or not the case was deleted
        return True if case else False


