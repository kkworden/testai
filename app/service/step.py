from app.model import Step, TestCase

ALLOWED_STEP_TYPE = ['action', 'assertion']


class StepService:
    '''
    A class to handle all Step operations.
    '''

    def __init__(self, db_session):
        self.db_session = db_session

    def create(self, test_case_id, contents, step_type):
        '''
        Creates a test case step.

        Request parameters:
            test_case_id: The id of the test case to attach this step to.
            contents: The assertion/action of the step.
            step_type: The type of step that this is (either "assertion" or "action").
        '''
        # Check if the test case the user wants to attach this step to is valid.
        case = self.db_session.get(TestCase, test_case_id)
        if not case:
            raise ValueError('Not a valid test case.')

        # Check the step type
        if step_type not in ALLOWED_STEP_TYPE:
            raise ValueError(f'step_type must be one of {ALLOWED_STEP_TYPE}')

        new_step = Step(test_case_id=test_case_id, contents=contents, type=step_type)

        # Commit to the database
        self.db_session.add(new_step)
        self.db_session.commit()

        self.db_session.refresh(new_step)

        # Return a success message with the id
        return new_step

    def edit(self, step_id, **kwargs):
        '''
        Updates a test case step's values.

        Request parameters:
            step_id: The id of the step to update.
            test_case_id: The id of the test case to attach this step to.
            contents: The assertion/action of the step.
            step_type: The type of step that this is (either "assertion" or "action").
        '''

        case = self.db_session.get(Step, step_id)
        changed = False

        # Update provided fields
        if 'step_type' in kwargs:
            case.type = kwargs['step_type']

            # Check the step type
            if kwargs['step_type'] not in ALLOWED_STEP_TYPE:
                raise ValueError(f'step_type must be one of {ALLOWED_STEP_TYPE}')

            changed = True
        if 'contents' in kwargs:
            case.contents = kwargs['contents']
            changed = True
        if 'test_case_id' in kwargs:
            case.test_case_id = kwargs['test_case_id']
            changed = True

        # Commit to the database
        self.db_session.commit()

        # Return whether or not something changed
        return changed

    def delete(self, step_id):
        '''
        Deletes a test case step.

        Request parameters:
            step_id: The id of the test case step.
        '''
        step = self.db_session.get(Step, step_id)
        if step:
            self.db_session.delete(step)
            self.db_session.commit()

        # Return a success message with a boolean describing whether or not the step was actually deleted
        return True if step else False
