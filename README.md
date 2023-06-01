# My Project

This project is a web application developed using Python and FastAPI. It provides a GraphQL endpoint for accessing standards and files. The application interacts with a database using the `MyDb` class to retrieve and store data.

## Installation

1. Clone the repository: `git clone https://github.com/SebDeclercq/fastapi-sqlalchemy-strawberry-asyncio`
2. Install the dependencies: `pip install -r requirements.txt`

## Usage

The project provides a main module `__main__.py` that can be executed to start the FastAPI application. The `main()` function initializes the application and returns the FastAPI instance.

To start the application, run the following command:

`python -m standards`

The application will start running on a local server at `http://localhost:8000`.

## Website Functionality

The website provides the following features:

### GraphQL API

The application exposes a GraphQL endpoint that allows querying and mutation operations to interact with the standards and files data. You can use tools like GraphiQL or GraphQL Playground to interact with the API.

The GraphQL endpoint URL is `http://localhost:8000/graphql`.

### Standards

- Retrieve a single standard by its `numdos` identifier.
  - URL endpoint: `GET /standards/{numdos}`
- Retrieve a list of all standards.
  - URL endpoint: `GET /standards`

### Files

- Retrieve a single file by its `numdos` and `numdosvl` identifiers.
  - URL endpoint: `GET /files/{numdos}/{numdosvl}`
- Retrieve a list of all files.
  - URL endpoint: `GET /files`

## Project Structure

The project has the following structure:

- `standards/`: The root directory of the package.
  - `_private/`: A private module that contains internal implementation details.
    - `__init__.py`: Initialization file for the private module.
    - `enum.py`: Module defining custom enumeration classes.
    - `pydantic.py`: Module defining Pydantic configuration.
    - `types.py`: Module defining custom type aliases and type hints.
  - `db/`: Module for working with the database.
    - `__init__.py`: Initialization file for the database module.
    - `models.py`: Module defining database models for standards and files.
  - `graphql/`: Module for handling GraphQL queries and types.
    - `__init__.py`: Initialization file for the GraphQL module.
    - `queries.py`: Module defining GraphQL queries for retrieving standards and files.
    - `types.py`: Module defining custom GraphQL types and type resolvers.
  - `__init__.py`: Initialization file for the standards package.
  - `__main__.py`: Main entry point of the package.


## Testing

The project includes unit tests to ensure the correctness of the application.
Don't forget to install the dependencies: `pip install -r requirements-dev.txt`.

You can run the tests using the following command:

`pytest`

Make sure to install the testing dependencies specified in `requirements.txt` before running the tests.
