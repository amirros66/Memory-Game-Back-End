Don't forget this!:

# Create a new env

$ python -m venv .venv

# Activate the env

$ source .venv/bin/activate

$ pipenv install sqlalchemy pydantic fastapi "uvicorn[standard]"

# set up Docker container

docker run --name memorydb -d -p 5432:5432 -e POSTGRES_PASSWORD=secret postgres
