# Standards

This project is a web application developed using Python and FastAPI. It provides a GraphQL endpoint for accessing standards and files. The application interacts with a database using the `MyDb` class to retrieve and store data.

## Installation

1. Clone the repository: `git clone https://github.com/SebDeclercq/fastapi-sqlalchemy-strawberry-asyncio`
2. Install the dependencies: `pip install -r requirements.txt`

## Usage

### Standards CLI

A command-line interface (CLI) tool for the Standards package.

To run the Standards CLI, use the following command:

```shell
python -m standards [command]
```

Replace `[command]` with one of the available commands described below.

#### Commands

- **runserver**

Command to start the server using uvicorn.

Usage:

```shell
python -m standards runserver
```

Options:

- `--host <host:str>`: The host address to bind the server (default: 0.0.0.0).
- `--port <port:int>`: The port number to bind the server (default: 8000).

The application will start running on a local server at `http://0.0.0.0:8000` by default.

- **random_populate**

Command to populate the database with random data.

Usage:

```shell
python -m standards random_populate
```

Options:

- `--db-url <db_url:str>`: The URL of the database to populate.
- `--count <count:int>`: The number of records to populate (default: 10).


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
  - `commands/`: Module for defining CLI commands.
    - `__init__.py`: Initialization file for the commands module.
    - `random_populate.py`: Module defining the random_populate command
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
