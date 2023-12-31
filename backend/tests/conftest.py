import warnings
import os
import random
from typing import List, Callable

import pytest
import pytest_asyncio
from fastapi import FastAPI
from async_asgi_testclient import TestClient
from databases import Database

import alembic
from alembic.config import Config

from app.core.config import SECRET_KEY, JWT_TOKEN_PREFIX
from app.services import auth_service

from app.models.cleaning import CleaningCreate, CleaningInDB
from app.db.repositories.cleanings import CleaningsRepository

from app.models.user import UserCreate, UserInDB
from app.db.repositories.users import UsersRepository

from app.models.offer import OfferCreate
from app.db.repositories.offers import OffersRepository

from app.models.evaluation import EvaluationCreate
from app.db.repositories.evaluations import EvaluationsRepository


async def user_fixture_helper(*, db: Database, new_user: UserCreate) -> UserInDB:
    user_repo = UsersRepository(db)
    existing_user = await user_repo.get_user_by_email(email=new_user.email)
    if existing_user:
        return existing_user
    return await user_repo.register_new_user(new_user=new_user)


async def create_cleaning_with_evaluated_offer_helper(
        db: Database,
        owner: UserInDB,
        cleaner: UserInDB,
        cleaning_create: CleaningCreate,
        evaluation_create: EvaluationCreate,
) -> CleaningInDB:
    cleaning_repo = CleaningsRepository(db)
    offers_repo = OffersRepository(db)
    evals_repo = EvaluationsRepository(db)
    created_cleaning = await cleaning_repo.create_cleaning(new_cleaning=cleaning_create, requesting_user=owner)
    offer = await offers_repo.create_offer_for_cleaning(
        new_offer=OfferCreate(cleaning_id=created_cleaning.id, user_id=cleaner.id),
        requesting_user=cleaner,
    )
    await offers_repo.accept_offer(offer=offer)
    await evals_repo.create_evaluation_for_cleaner(
        evaluation_create=evaluation_create, cleaning=created_cleaning, cleaner=cleaner,
    )
    return created_cleaning


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
def authorized_client(client: TestClient, test_user: UserInDB) -> TestClient:
    access_token = auth_service.create_access_token_for_user(user=test_user, secret_key=str(SECRET_KEY))
    client.headers = {
        **client.headers,
        "Authorization": f"{JWT_TOKEN_PREFIX} {access_token}",
    }
    return client


@pytest_asyncio.fixture
def create_authorized_client(client: TestClient) -> Callable:
    def _create_authorized_client(*, user: UserInDB) -> TestClient:
        access_token = auth_service.create_access_token_for_user(user=user, secret_key=str(SECRET_KEY))
        client.headers = {
            **client.headers,
            "Authorization": f"{JWT_TOKEN_PREFIX} {access_token}",
        }
        return client
    
    return _create_authorized_client


@pytest_asyncio.fixture
async def test_cleaning(db: Database, test_user: UserInDB) -> CleaningInDB:
    cleaning_repo = CleaningsRepository(db)
    new_cleaning = CleaningCreate(
        name="fake cleaning name", description="fake cleaning description", price=9.99, cleaning_type="spot_clean"
    )
    
    return await cleaning_repo.create_cleaning(new_cleaning=new_cleaning, requesting_user=test_user)


@pytest_asyncio.fixture
async def test_cleaning_with_offers(db: Database, test_user2: UserInDB, test_user_list: List[UserInDB]) -> CleaningInDB:
    cleaning_repo = CleaningsRepository(db)
    offers_repo = OffersRepository(db)
    new_cleaning = CleaningCreate(
        name="cleaning with offers", description="desc for cleaning", price=9.99, cleaning_type="full_clean",
    )
    created_cleaning = await cleaning_repo.create_cleaning(new_cleaning=new_cleaning, requesting_user=test_user2)
    for user in test_user_list:
        await offers_repo.create_offer_for_cleaning(
            new_offer=OfferCreate(cleaning_id=created_cleaning.id, user_id=user.id),
            requesting_user=user,
        )
    
    return created_cleaning


@pytest_asyncio.fixture
async def test_cleaning_with_accepted_offer(
        db: Database, test_user2: UserInDB, test_user3: UserInDB, test_user_list: List[UserInDB]
) -> CleaningInDB:
    cleaning_repo = CleaningsRepository(db)
    offers_repo = OffersRepository(db)
    
    new_cleaning = CleaningCreate(
        name="cleaning with offers", description="desc for cleaning", price=9.99, cleaning_type="full_clean",
    )
    
    created_cleaning = await cleaning_repo.create_cleaning(new_cleaning=new_cleaning, requesting_user=test_user2)
    
    offers = []
    for user in test_user_list:
        offers.append(
            await offers_repo.create_offer_for_cleaning(
                new_offer=OfferCreate(cleaning_id=created_cleaning.id, user_id=user.id),
                requesting_user=user,
            )
        )
    
    await offers_repo.accept_offer(
        offer=[o for o in offers if o.user_id == test_user3.id][0]
    )
    
    return created_cleaning


@pytest_asyncio.fixture
async def test_list_of_cleanings_with_evaluated_offer(
        db: Database, test_user2: UserInDB, test_user3: UserInDB,
) -> List[CleaningInDB]:
    return [
        await create_cleaning_with_evaluated_offer_helper(
            db=db,
            owner=test_user2,
            cleaner=test_user3,
            cleaning_create=CleaningCreate(
                name=f"test cleaning - {i}",
                description=f"test description - {i}",
                price=float(f"{i}9.99"),
                cleaning_type="full_clean",
            ),
            evaluation_create=EvaluationCreate(
                professionalism=random.randint(0, 5),
                completeness=random.randint(0, 5),
                efficiency=random.randint(0, 5),
                overall_rating=random.randint(0, 5),
                headline=f"test headline - {i}",
                comment=f"test comment - {i}",
            ),
        )
        for i in range(5)
    ]


@pytest_asyncio.fixture
async def test_list_of_cleanings_with_pending_offers(
        db: Database, test_user: UserInDB, test_user_list: List[UserInDB]
) -> List[CleaningInDB]:
    cleaning_repo = CleaningsRepository(db)
    offers_repo = OffersRepository(db)
    cleanings = []
    for i in range(5):
        created_cleaning = await cleaning_repo.create_cleaning(
            new_cleaning=CleaningCreate(
                name=f"test cleaning with offers - {i}",
                description=f"test desc for cleaning with offers - {i}",
                price=float(f"{i}9.99"),
                cleaning_type="spot_clean",
            ),
            requesting_user=test_user,
        )
        for user in test_user_list:
            await offers_repo.create_offer_for_cleaning(
                new_offer=OfferCreate(cleaning_id=created_cleaning.id, user_id=user.id),
                requesting_user=user,
            )
        cleanings.append(created_cleaning)
    return cleanings


@pytest_asyncio.fixture
async def test_user(db: Database) -> UserInDB:
    new_user = UserCreate(email="harry@kane.com", username="harrykane", password="tottenham")
    return await user_fixture_helper(db=db, new_user=new_user)


@pytest_asyncio.fixture
async def test_user2(db: Database) -> UserInDB:
    new_user = UserCreate(email="marcus@rashford.com", username="marcusrashford", password="manchesterunited")
    return await user_fixture_helper(db=db, new_user=new_user)


@pytest_asyncio.fixture
async def test_user3(db: Database) -> UserInDB:
    new_user = UserCreate(email="moha@salah.com", username="mohasalah", password="liverpool")
    return await user_fixture_helper(db=db, new_user=new_user)


@pytest_asyncio.fixture
async def test_user4(db: Database) -> UserInDB:
    new_user = UserCreate(email="bukayo@saka.com", username="bukayosaka", password="arsenalfc")
    return await user_fixture_helper(db=db, new_user=new_user)


@pytest_asyncio.fixture
async def test_user5(db: Database) -> UserInDB:
    new_user = UserCreate(email="enzo@fernandez.com", username="enzofernandez", password="chelseafc")
    return await user_fixture_helper(db=db, new_user=new_user)


@pytest_asyncio.fixture
async def test_user6(db: Database) -> UserInDB:
    new_user = UserCreate(email="kevin@debruyne.com", username="kevindebruyne", password="manchestercity")
    return await user_fixture_helper(db=db, new_user=new_user)


@pytest_asyncio.fixture
async def test_user_list(
        test_user3: UserInDB, test_user4: UserInDB, test_user5: UserInDB, test_user6: UserInDB,
) -> List[UserInDB]:
    return [test_user3, test_user4, test_user5, test_user6]
