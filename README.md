# NYU DevOps Project Template

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

[![codecov](https://codecov.io/gh/CSCI-GA-2820-SU23-001/customers/branch/master/graph/badge.svg?token=L9SLZ9KEXM)](https://codecov.io/gh/CSCI-GA-2820-SU23-001/customers)
[![Build Status](https://github.com/CSCI-GA-2820-SU23-001/customers/actions/workflows/tdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-SU23-001/customers/actions)
[![Build Status](https://github.com/CSCI-GA-2820-SU23-001/customers/actions/workflows/bdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-SU23-001/customers/actions)


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

## Running the service

The project uses *honcho* which gets it's commands from the `Procfile`. To start the service:

```shell
$ honcho start
```

You could reach the service at: http://localhost:8000 as defined in the `.flaskenv` file, which Flask uses to load it's configuration from the environment by default.

## Customer Service APIs

### Customer Operations

| Endpoint          | Methods | Rule
| ---------------   | ------- | --------------------------
| create_customers  | POST    | ```/customers```
| get_customers     | GET     | ```/customers/{int:customer_id}```
| update_customers  | PUT     | ```/customers/{int:customer_id}```
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
  "password": "password",
  "available": True
}


```

Success Response : `HTTP_200_CREATED`
```
[
  {
    "id":1,
    "name": "John Doe",
    "address": "5th Fifth Ave, NY",
    "email": "john@gmail.com",
    "phone_number": "12345678",
    "password": "password",
    "available": True
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
    "password": "password",
    "available": True
}
]
```

Failure Response : `HTTP_404_NOT_FOUND`
```
{
  "error": "Not Found",
  "message": "404 Not Found: Customer with id '3' was not found.",
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
    "name": "John Foo",
    "address": "5th Fifth Ave, NY",
    "email": "john@gmail.com",
    "phone_number": "12345678",
    "password": "password",
    "available": True
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
    "password": "password",
    "available": True
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

This is the planned version of listing customers. Currently the listing part still have some errors

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
    "password": "password",
    "available": True
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
└── static                 - static code package
    ├── css                - UI page format
    ├── images             - UI page mage
    ├── js                 - UI page constants
    └── index.html         - UI page alignment

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
