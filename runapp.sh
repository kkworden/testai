export FLASK_APP=app
export FLASK_ENV=development
export TEST_DATABASE_DIR=$(pwd)
pipenv install
pipenv run flask run
