# Propylon Document Manager Assessment

## API 

run `docker build . --platform="linux/amd64" -t app`

This will create a user for you with email `test@email.com` and password `123456`.

run `docker run -p 8001:8001 -it app`

Grab your token with this curl
```
curl --location 'http://localhost:8001/auth-token/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "test@email.com",
    "password": "123456"
}'
```

1. Go to http://localhost:8001/api/docs/
2. Click "Authorize" button in the top right
3. Enter your token from the above curl command and make sure you prefix it with "Token "
4. Play around with endpoints


## UI
I did not get to finish the ui, only added a small bit but if you would like to take a look you can add your same token
from above to line 64 of FileVersions.js

Run
`cd client/doc-manager/`
`npm install`
`npm start`

You can go to http://localhost:3000
You can upload/download files at whichever url you.

## Requirements overview
Stores files of any type and name 
- Stores files at any URL 
  - File table uses a location field to track at which URL the file is saved
- Does not allow interaction by non-authenticated users 
  - Implemented with token authentication
- Does not allow a user to access files submitted by another user 
  - Files are filtered down by authenticated user
- Allows users to store multiple revisions of the same file at the same URL 
  - File version will increment when the "same file" is uploaded. Files are the same if they share the same location, file_name, and extension. Not by content
- Allows users to fetch any revision of any file 
  - All file versions are listed in each location
- Demonstrate functionality that allows a client to retrieve any given version of document using a endpoint that implements a Content Addressable Storage mechanism.
  - You can query `/api/files/` with `content_md5` which will give you any files that have the exact same content.


___

# Original readme

The Propylon Document Management Technical Assessment is a simple (and incomplete) web application consisting of a basic API backend and a React based client.  This API/client can be used as a bootstrap to implement the specific features requested in the assessment description. 

## Getting Started
1. [Install Direnv](https://direnv.net/docs/installation.html)
2. [Install Pipenv](https://pipenv.pypa.io/en/latest/installation/)
3. This project requires Python 3.11 so you will need to ensure that this version of Python is installed on your OS before building the virtual environment.
4. `$ cp example.env .envrc`
5. `$ direnv allow .`
6. `$ pipenv install -r requirements/local.txt`.  If Python 3.11 is not the default Python version on your system you may need to explicitly create the virtual environment (`$ python3.11 -m venv .venv`) prior to running the install command. 
7. `$ pipenv run python manage.py migrate` to create the database.
8. `$ pipenv run python manage.py load_file_fixtures` to create the fixture file versions.
9. `$ pipenv run python manage.py runserver 0.0.0.0:8001` to start the development server on port 8001.
10. Navigate to the client/doc-manager directory.
11. `$ npm install` to install the dependencies.
12. `$ npm start` to start the React development server.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

### Type checks

Running type checks with mypy:

    $ mypy propylon_document_manager

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest
