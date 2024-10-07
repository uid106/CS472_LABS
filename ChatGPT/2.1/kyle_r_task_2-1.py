# My tests for the flask counter from the tdd lab
"""
Test Cases for Counter Web Service
Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
import pytest

# used for creating unique counter identifiers, would need to be added to requirements.txt
import uuid

# we need to import the unit under test - counter
from src.counter import app 

# we need to import the file that contains the status codes
from src import status 

@pytest.fixture()
def client():
    return app.test_client()

@pytest.fixture()
def unique_counter_name():
    """Generate a unique counter name for testing."""
    return f"counter-{uuid.uuid4()}"

@pytest.mark.usefixtures("client")
class TestCounterEndPoints:
    """Test cases for Counter-related endpoints"""

    def create_counter(self, client, counter_name):
        return client.post(f'/counters/{counter_name}')

    def get_counter(self, client, counter_name):
        return client.get(f'/counters/{counter_name}')

    def update_counter(self, client, counter_name):
        return client.put(f'/counters/{counter_name}')

    def delete_counter(self, client, counter_name):
        return client.delete(f'/counters/{counter_name}')

    def test_create_a_counter(self, client, unique_counter_name):
        """It should create a counter"""
        result = self.create_counter(client, unique_counter_name)
        assert result.status_code == status.HTTP_201_CREATED     

    def test_duplicate_a_counter(self, client, unique_counter_name):
        """It should return an error for duplicates"""
        self.create_counter(client, unique_counter_name)
        result = self.create_counter(client, unique_counter_name)
        assert result.status_code == status.HTTP_409_CONFLICT
    
    def test_update_a_counter(self, client, unique_counter_name):
        self.create_counter(client, unique_counter_name)
        result = self.update_counter(client, unique_counter_name)
        assert result.status_code == status.HTTP_200_OK
        new_count = result.json[unique_counter_name]
        assert new_count == 1  # Assuming the counter increments by 1

    def test_get_counter(self, client, unique_counter_name):
        self.create_counter(client, unique_counter_name)
        result = self.get_counter(client, unique_counter_name)
        assert result.status_code == status.HTTP_200_OK
        assert result.json[unique_counter_name] == 0  # Assuming initial value is 0

    def test_del_counter(self, client, unique_counter_name):
        self.create_counter(client, unique_counter_name)
        result = self.delete_counter(client, unique_counter_name)
        assert result.status_code == status.HTTP_204_NO_CONTENT
        result = self.get_counter(client, unique_counter_name)
        assert result.status_code == status.HTTP_404_NOT_FOUND

    def test_del_counter_not_present(self, client):
        counter_name = f'counter-{uuid.uuid4()}'
        result = self.delete_counter(client, counter_name)
        assert result.status_code == status.HTTP_404_NOT_FOUND
