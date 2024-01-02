# Hello there! 

This is an API to manage StarWars Characters data. 

The information is stored in a SQLite DB and the API built with FastAPI.


In order to run the API you can use Docker or do the step by step yourself:

# Using Docker:
- If you don't have Docker installed in your computer, download and install it from https://docs.docker.com/get-docker/.
- Clone the repo.
- Open the repo folder in VSCode or your preferred editor.
- Open a terminal on the project folder and run:  docker compose up --build
- If the container was built successfully you should have an hyperlink in stating:  Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
- Open a browser in LocalHost ( http://0.0.0.0:8000 ). You will see the Swagger documentation displayed at the home url where you can test some scenarios.


# Without Docker:
- If you prefer to build the resources on your own:
- Clone the repo.
- Open the repo folder in VSCode or your preferred editor.
- Install Uvicorn, FastAPI and SQLALchemy by opening a terminal on the project folder and running: pip install -r requirements.txt
- Launch the App at the Uvicorn Server by running:   uvicorn main:app --reload  --port=8000 --host=0.0.0.0
- Open a browser in LocalHost ( http://0.0.0.0:8000 ). You will see the Swagger documentation displayed at the home url where you can test some scenarios.


# IMPORTANT:   
The LocalHost should address should not be in use by other container or app. If this would happen  you will get an error message describing the port is not free to use. In such scenario use a different port.

