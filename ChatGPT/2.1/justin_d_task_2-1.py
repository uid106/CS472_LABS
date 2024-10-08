import json
from random import randrange
import pytest
from models import db, app
from models.account import Account, DataValidationError

# Global variable to store account data
ACCOUNT_DATA = {}


# ---------- FIXTURES ----------
@pytest.fixture(scope="module", autouse=True)
def load_account_data():
    """ Load data needed by tests and set up the database """
    global ACCOUNT_DATA
    with open('tests/fixtures/account_data.json') as json_data:
        ACCOUNT_DATA = json.load(json_data)

    db.create_all()  # Initialize the database
    yield
    db.session.close()  # Clean up after tests


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """ Truncate the tables before each test """
    db.session.query(Account).delete()
    db.session.commit()
    yield
    db.session.remove()  # Clean up the session after each test


# ---------- TEST CASES ----------
def test_create_all_accounts():
    """ Test creating multiple Accounts """
    for data in ACCOUNT_DATA:
        account = Account(**data)
        account.create()
    assert len(Account.all()) == len(ACCOUNT_DATA)


def test_create_single_account():
    """ Test Account creation using random data """
    data = random_account_data()
    account = Account(**data)
    account.create()
    assert len(Account.all()) == 1


def test_account_representation():
    """Test the string representation of an account"""
    account = Account(name="Foo")
    assert str(account) == "<Account 'Foo'>"


def test_account_to_dict():
    """ Test converting an account to a dictionary """
    account = Account(**random_account_data())
    result = account.to_dict()

    assert result == {
        "name": account.name,
        "email": account.email,
        "phone_number": account.phone_number,
        "disabled": account.disabled,
        "date_joined": account.date_joined
    }


def test_account_from_dict():
    """ Test creating an Account from a dictionary """
    data = {
        "name": "Test Account",
        "email": "test@example.com",
    }
    account = Account().from_dict(data)

    assert account.name == data["name"]
    assert account.email == data["email"]


def test_create_account_in_database():
    """ Test persisting an Account to the database """
    account = Account(name="Test Account", email="test@example.com")
    account.create()

    # Verify the account is in the database
    fetched_account = Account.find(account.id)
    assert fetched_account.name == "Test Account"
    assert fetched_account.email == "test@example.com"


def test_update_account():
    """ Test updating an Account's details """
    account = Account(name="Original Account", email="original@example.com")
    account.create()

    account.name = "Updated Account"
    account.update()

    # Verify the account was updated
    updated_account = Account.find(account.id)
    assert updated_account.name == "Updated Account"


def test_update_account_without_id():
    """ Test updating an Account without an ID raises an error """
    account = Account(name="Uncommitted Account")

    with pytest.raises(DataValidationError):
        account.update()  # Should raise DataValidationError


def test_delete_account():
    """ Test deleting an Account from the database """
    account = Account(name="Delete Account", email="delete@example.com", balance=100)
    account.create()

    account_id = account.id
    account.delete()

    # Verify the account is deleted
    assert Account.find(account_id) is None


def test_fetch_all_accounts():
    """ Test retrieving all Accounts """
    account1 = Account(name="Account 1", email="account1@example.com", balance=100)
    account2 = Account(name="Account 2", email="account2@example.com", balance=200)
    account1.create()
    account2.create()

    accounts = Account.all()
    assert len(accounts) == 2


def test_find_account_by_id():
    """ Test finding an Account by ID """
    account = Account(name="Find Account", email="find@example.com", balance=100)
    account.create()

    fetched_account = Account.find(account.id)
    assert fetched_account is not None
    assert fetched_account.id == account.id
    assert fetched_account.name == "Find Account"


def test_find_nonexistent_account():
    """ Test finding a non-existent Account """
    account = Account.find(9999)  # Non-existent ID
    assert account is None


# ---------- HELPER FUNCTIONS ----------
def random_account_data():
    """ Returns random account data from the fixture """
    rand = randrange(0, len(ACCOUNT_DATA))
    return ACCOUNT_DATA[rand]
