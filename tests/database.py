import os

import pytest



from fastapi.testclient import TestClient
from FastAPI90.main import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from FastAPI90.config import settings
from FastAPI90.database import get_db
from FastAPI90 import models  # Make sure this contains your SQLAlchemy models
from FastAPI90.database import engine
from FastAPI90.database import Base





#'postgresql://<username>:<password>@<ip-adress/hostname>/<database_name>
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/test'


#creating an engine to connect to our server
test_engine = create_engine(SQLALCHEMY_DATABASE_URL)


#just copying default documentation from FASTAPI
TestingSessionLocal = sessionmaker(autocommit = False,autoflush = False,bind = test_engine)