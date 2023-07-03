import warnings
import os

import pytest

from fastapi import FastAPI
from async_asgi_testclient import TestClient
import pytest_asyncio
from databases import Database

from app.core.config import SECRET_KEY, JWT_TOKEN_PREFIX
from app.services import auth_service

from app.models.cleaning import CleaningCreate, CleaningInDB
from app.db.repositories.cleanings import CleaningsRepository

from app.models.user import UserCreate, UserInDB
from app.db.repositories.users import UsersRepository

import alembic
from alembic.config import Config


# Apply migrations at beginning and end of testing session
@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")
    
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


# Create a new application for testing
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.api.server import get_application
    
    return get_application()


# Grab a reference to our database when needed
@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


@pytest_asyncio.fixture
async def client(app: FastAPI) -> TestClient:
    async with TestClient(app, headers={"Content-Type": "application/json"}) as client:
        yield client


@pytest_asyncio.fixture
async def test_user(db: Database) -> UserInDB:
    new_user = UserCreate(
        email="example@mail.com",
        username="example",
        password="longpassword",
    )
    user_repo = UsersRepository(db)
    
    existing_user = await user_repo.get_user_by_email(email=new_user.email)
    if existing_user:
        return existing_user
    return await user_repo.register_new_user(new_user=new_user)


@pytest_asyncio.fixture
def authorized_client(client: TestClient, test_user: UserInDB) -> TestClient:
    access_token = auth_service.create_access_token_for_user(user=test_user, secret_key=str(SECRET_KEY))
    client.headers = {
        **client.headers,
        "Authorization": f"{JWT_TOKEN_PREFIX} {access_token}",
    }
    return client


@pytest_asyncio.fixture
async def test_user2(db: Database) -> UserInDB:
    new_user = UserCreate(
        email="david@jones.com",
        username="davidjones",
        password="piratesofcaribean",
    )
    user_repo = UsersRepository(db)
    existing_user = await user_repo.get_user_by_email(email=new_user.email)
    
    if existing_user:
        return existing_user
    return await user_repo.register_new_user(new_user=new_user)


@pytest_asyncio.fixture
async def test_cleaning(db: Database, test_user: UserInDB) -> CleaningInDB:
    cleaning_repo = CleaningsRepository(db)
    new_cleaning = CleaningCreate(
        name="fake cleaning name", description="fake cleaning description", price=9.99, cleaning_type="spot_clean"
    )
    
    return await cleaning_repo.create_cleaning(new_cleaning=new_cleaning, requesting_user=test_user)
