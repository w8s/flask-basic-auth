# Basic Auth in Flask

A simple implementation of how to implement basic auth in Flask without additional libraries.

## Instructions to Run

* Create a `virtualenv`
* With `env` activated, run `pip install -r requirements.txt`
* Run `export FLASK_APP=auth.py flask init` to populate the database.
* Run `export FLASK_APP=auth.py flask run` to run the application.

## Examples

The repository is tagged at each commit with what example is implemented.

1. Basic Auth with Hardcoded Username and Password.
2. Basic Auth with Database Users with Plain Text Passwords.
3. Basic Auth with Database Users with encrypted passwords.
