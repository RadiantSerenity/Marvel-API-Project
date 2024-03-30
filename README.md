# Marvel API Server Documentation

## Introduction

The `api_server.py` script establishes a local API server that interacts with a `data.csv` file, containing a list of 30 Marvel characters along with detailed attributes like character name, ID, available events, series, comics, and the price of the most expensive comic per character. The script `client_enhanced.py` demonstrates the API's functionality through various example requests.

## Basic Functions

The API supports multiple functionalities:

- **GET Request**: Retrieve character information.
- **POST Request**: Add new characters with either complete or partial information (missing details are fetched from the Marvel API).
- **DELETE Request**: Remove characters from the database.
- **PUT Request**: Modify the price of a character's most expensive comic, integrating an exchange rate adjuster.
- **Authentication (Not Implemented Yet)**: Signup, login, and OAuth features are planned but currently not available.

## Requirements

Ensure the following are installed to use the API server:

- Python 3.x
- Flask
- Pandas
- Requests
- Flask-RESTful components (Resource, Api, reqparse)

## Starting the API Server

1. Modify the working directory path in `api_server.py` (line 55) to include `data.csv` and related files.
2. Navigate to the directory in your command console (`cd "your path here"`).
3. Start the server using `python api_server.py`, which runs on http://localhost:5000/.
4. To test, run `python client_enhanced.py` in a separate console after adjusting the directory path.

## Using the API

### Endpoints

The API has a single endpoint, `/characters`, supporting various operations:

- **GET `/characters`**: Fetches the entire DataFrame as JSON.
- **GET `/characters/"id_or_name"`**: Retrieves data for specific characters by ID or name.
- **POST `/characters"`**: Adds a new character with full details to the DataFrame. Duplicate Character IDs are not allowed.
- **POST `/characters/"id"`**: Adds a character by ID, fetching missing details from the Marvel API. Returns an error if the ID is not found.
- **DELETE `/characters/"id_or_name"`**: Deletes characters by ID or name. Errors if characters do not exist.
- **PUT `/characters/"id_or_name"`**: Adjusts the price of the most expensive comic for specified characters by ID or name.

## Warnings!

POST requests with incomplete information depend on the Marvel API, which is in beta and may return unexpected errors.
