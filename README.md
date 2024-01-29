Don't forget this!: 

# Create a new env
$ python -m venv .venv

# Activate the env
$ source .venv/bin/activate

$ pipenv install sqlalchemy pydantic fastapi "uvicorn[standard]"

# set up Docker container
docker run --name memorydb -d -p 5432:5432 -e POSTGRES_PASSWORD=secret postgres
ed4d2de40435658d0bedf9e946a154f7be4a00186e57d6e5884b8f082cbeaa85 


