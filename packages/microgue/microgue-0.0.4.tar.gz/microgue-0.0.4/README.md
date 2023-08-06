# Flask Microservice Bootstrap Code Project

This project contains bootstrap code to speed up the development of Flask based microservices by providing code to connect to a variety of AWS services

This includes:
- Redis Cache
- Kinesis Event Streams
- DynamoDB Models and Model Objects
- SQS Queues
- Secrets Manager
- S3 Storage

This project also includes base code for:
- Object Definitions
- Service Connections
- Flask App Definitions
- Additional Utilities


### Requirements

- You have Python 3.6 installed as `python3`

    - Verify with `python3 --version`

### Pre-Setup

- Make sure you have an IAM user created with correct permissions in your AWS account

    - Create an Access Key on that user

    - Install awscli `pip install awscli`

    - Add that Access Key with `aws configure`

    - Verify you are using the correct Access Key with `aws configure list`

### Minimum Setup

- Put the following code in the app.py file in the root of the project

```python
from microgue.abstract_app import AbstractApp


class App(AbstractApp):
    pass


app = App().app

```

- In the terminal run the following commands

```
export PYTHONUNBUFFERED=1
export FLASK_DEBUG=1
flask run
```

- GET http://127.0.0.1:5000

### Distribution
```
# package with:
python setup.py sdist bdist_wheel

# uploade to test pypi with:
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# uploade to pypi with:
python -m twine upload dist/*

# uploade to pypi with:
python -m twine upload dist/*
```

### Problems

- Wrong version for python3:

    - Try installing `pyenv`, which allows you to manage multiple version of python on one machine

        - ```
          # intall dependencies
          brew install openssl readline sqlite3 xz zlib

          # install pyenv
          curl https://pyenv.run | bash

          # add these next three lines to your bash_profile (assuming you use bash)
          export PATH="$HOME/.pyenv/bin:$PATH"
          eval "$(pyenv init -)"
          eval "$(pyenv virtualenv-init -)"

          # install python 3.6.10
          pyenv install 3.6.10

          # get the path to python 3.6.10 to be used when creating the virtual environment
          which ~/.pyenv/versions/3.6.10/bin/python
          ```
