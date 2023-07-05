# NYU DevOps Project Template

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

This is a skeleton you can use to start your projects

## Overview

This project template contains starter code for your class project. The `/service` folder contains your `models.py` file for your model and a `routes.py` file for your service. The `/tests` folder has test case starter code for testing the model and the service separately. All you need to do is add your functionality. You can use the [lab-flask-tdd](https://github.com/nyu-devops/lab-flask-tdd) for code examples to copy from.

## Automatic Setup

The best way to use this repo is to start your own repo using it as a git template. To do this just press the green **Use this template** button in GitHub and this will become the source for your repository.

## Manual Setup

You can also clone this repository and then copy and paste the starter code into your project repo folder on your local computer. Be careful not to copy over your own `README.md` file so be selective in what you copy.

There are 4 hidden files that you will need to copy manually if you use the Mac Finder or Windows Explorer to copy files from this folder into your repo folder.

These should be copied using a bash shell as follows:

```bash
    cp .gitignore  ../<your_repo_folder>/
    cp .flaskenv ../<your_repo_folder>/
    cp .gitattributes ../<your_repo_folder>/
```

## Customer Service APIs

### Customer Operations

| Endpoint          | Methods | Rule
| ---------------   | ------- | --------------------------
| create_a_customer | POST    | ```/customers```
| read_a_customer   | GET     | ```/customers/{int:customer_id}```
| update_a_customer | PUT     | ```/customers/{int:customer_id}```
| delete_a_customer | DELETE  | ```/customers/{int:customer_id}```
| list_customers    | GET     | ```/customers```

## APIs Usage

### Create a Customer
URL : `http://127.0.0.1:8000/customers`

Method : POST

Auth required : No

Permissions required : No

Create a customer using a JSON file that includes the customers's name, address, email, phone_number and password.

Example:

Request Body (JSON)
```
{
  "name": "John Doe",
  "address": "5th Fifth Ave, NY",
  "email": "john@gmail.com",
  "phone_number": "12345678",
  "password": "password"
}


```

Success Response : `HTTP_201_CREATED`
```
[
  {
    "id":1,
    "name": "John Doe",
    "address": "5th Fifth Ave, NY",
    "email": "john@gmail.com",
    "phone_number": "12345678",
    "password": "password"
}
]
```

### Read a Customer 

URL : `http://127.0.0.1:8000/customers/{int:customer_id}`

Method : GET

Auth required : No

Permissions required : No

Read all information of a customer with given id

Example:

Success Response : `HTTP_200_OK`
```
[
  {
    "id":1,
    "name": "John Doe",
    "address": "5th Fifth Ave, NY",
    "email": "john@gmail.com",
    "phone_number": "12345678",
    "password": "password"
}
]
```

Failure Response : `HTTP_404_NOT_FOUND`
```
{
  "error": "Not Found",
  "message": "404 Not Found: CUstomer with id '3' was not found.",
  "status": 404
}

```

### Update a Customer 


URL : `http://127.0.0.1:8000/customers/{int:customer_id}`

Method : PUT

Auth required : No

Permissions required : No

Updates a customer with id provided in the URL according to the updated fields provided in the body

Example:

Request Body (JSON)
```
  {
    "id":1,
    "name": "John Foo",
    "address": "5th Fifth Ave, NY",
    "email": "john@gmail.com",
    "phone_number": "12345678",
    "password": "password"
}
```


Success Response : `HTTP_200_OK`
```
[
  {
    "id":1,
    "name": "John Foo",
    "address": "5th Fifth Ave, NY",
    "email": "john@gmail.com",
    "phone_number": "12345678",
    "password": "password"
}
]

```

Failure Response : `HTTP_404_NOT_FOUND`
```
{
  "error": "Not Found",
  "message": "404 Not Found: Customer with id '2' was not found.",
  "status": 404
}

```

### Delete a Customer

URL : `http://127.0.0.1:8000/customers/{int:customer_id}`

Method : DELETE

Auth required : No

Permissions required : No

Deletes a Customer with id

Example:

Success Response : `204 NO CONTENT`


### List Customers

URL : `http://127.0.0.1:8000/customers` 

Method: GET

Auth required : No

Permissions required : No

List All Customers

Example:

Success Response : `HTTP_200_OK`

```
[
  {
    "id":1,
    "name": "John Foo",
    "address": "5th Fifth Ave, NY",
    "email": "john@gmail.com",
    "phone_number": "12345678",
    "password": "password"
}
]
```

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```

## Running the service

The project uses *honcho* which gets it's commands from the `Procfile`. To start the service:

```shell
$ honcho start
```

You could reach the service at: http://localhost:8000 as defined in the `.flaskenv` file, which Flask uses to load it's configuration from the environment by default.

To test and check the coverage: 
```shell
$ green
```

The result is supposed to be:

```
Name                               Stmts   Miss  Cover   Missing
----------------------------------------------------------------
service/__init__.py                   17      2    88%   31-32
service/common/cli_commands.py         7      0   100%
service/common/error_handlers.py      38      6    84%   77-79, 107-109
service/common/log_handlers.py        11      1    91%   35
service/common/status.py              45      0   100%
service/config.py                      5      0   100%
service/models.py                     59      0   100%
service/routes.py                     55      2    96%   117-118
----------------------------------------------------------------
TOTAL                                237     11    95%
```

Currently the listing api is still missing, once its work finishes, the pull request will be merged. Thus, the actual coverage of routes is expected to be higher.

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
