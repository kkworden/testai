# Test.ai Coding Assessment

This repository contains a basic Flask application that exposes a basic REST API for
creating test suites, cases, and steps.

## Running the app

To deploy the server: `./runapp.sh`

To run unit tests: `./runtests.sh`

## APIs

All APIs must be invoked using the `application/json` Content-Type. Parameters must live in a JSON
object in the request body.

All parameters described here are *required* unless the API description notes otherwise.

### GET `/`
**Description:** Dumps the database's contents out as JSON.

**Parameters:** (None)

### POST `/suite/create`
**Description:** Creates a *TestSuite*.

**Parameters:**
 * `name` - The name to give to the *TestSuite*.

### POST `/suite/edit`
**Description:** Edits a *TestSuite*.

**Parameters:**
 * `suite_id` - The id of the *TestSuite* to edit.
 * `name` (optional) - The name to give to the *TestSuite*.

### POST `/suite/delete`
**Description:** Deletes a *TestSuite*.

**Parameters:**
 * `suite_id` - The id of the *TestSuite* to delete.

### POST `/case/create`
**Description:** Creates a *TestCase*.

**Parameters:**
 * `test_suite_id` - The id of the *TestSuite* to attach this *TestCase* to.

### POST `/case/edit`
**Description:** Edits a *TestSuite*.

**Parameters:**
 * `case_id` - The id of the *TestCase* to edit.
 * `test_suite_id` (optional) - The id of the *TestSuite* to attach this *TestCase* to.

### POST `/case/delete`
**Description:** Deletes a *TestCase*.

**Parameters:**
 * `case_id` - The id of the *TestCase* to delete.

### POST `/step/create`
**Description:** Creates a *Step*.

**Parameters:**
 * `test_case_id` - The id of the *TestCase* to attach this *Step* to.
 * `contents` - A string representing what this *Step* will do.
 * `step_type` - The type of *Step* this is. Either "action" or "assertion".

### POST `/step/edit`
**Description:** Edits a *TestSuite*.

**Parameters:**
 * `step_id` - The id of the *Step* to edit.
 * `test_case_id` (optional) - The id of the *TestCase* to attach this *Step* to.
 * `contents` (optional) - A string representing what this *Step* will do.
 * `step_type` (optional) - The type of *Step* this is. Either "action" or "assertion".

### POST `/step/delete`
**Description:** Deletes a *Step*.

**Parameters:**
 * `step_id` - The id of the *Step* to delete.

## Data model
###TestSuite

**Description:** The highest-level construct in the application. A test suite is a container
for test cases. It takes a name as an identifier.

**Fields:**
 * `name` - The name of the test suite. Used for cosmetic purposes only. Non-unique.

###TestCase

**Description:** A test-case is a container of steps. A case must be contained in a *TestSuite*.

**Fields:**
 * `test_suite_id` - The id of the *TestSuite* that this case will belong to.

###Step

**Description:** A step is the lowest-level construct in the application. A step is meant
to represent a unit of logic to be run in a *TestCase*.

**Fields:**
 * `test_case_id` - The id of the *TestCase* that this step will belong to.
 * `contents` - Per the application spec, a step can either be an assertion or action, represented as a string.
    `contents` is a container for said string.
 * `step_type` - A string, either 'action' or 'assertion'.


## Shortcomings
Given that this assessment was only designed to take 2-3 hours, I didn't get to include
all features that I would like in a REST API. Some things I would have liked to include:

1. Input validation. I added basic input validation by checking for parameters, but sanitation
  to prevent HTML and SQL-injection would be a logical next step.
2. *Step* reordering. I assume that we would like to be able decide the order of *Step*s in a 
  *TestCase*.
3. Database configuration. I got a bare-bones database working with SQLite using SQLAlchemy.
  Setting up a database with SQLAlchemy is relatively straightforward, and would be a great improvement, 
  especially if this were to grow into a real application with lots of customers.
4. Authorization. Currently anyone can dump data from the database and create/edit/delete anything.
  Security is important and I didn't include it here!
5. The test coverage is not great. However, I feel that I got my point across for how I would go about testing
  additional classes.