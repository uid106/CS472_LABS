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

# we need to import the unit under test - counter
from src.counter import app 

# we need to import the file that contains the status codes
from src import status 

@pytest.fixture()
def client():
  return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndPoints:
    """Test cases for Counter-related endpoints"""

    def test_create_a_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED     

    def test_duplicate_a_counter(self, client):
        """It should return an error for duplicates"""
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_201_CREATED
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_409_CONFLICT
    
    def test_update_a_counter(self, client):
        result = client.post('/counters/testingUpdate')
        assert result.status_code == status.HTTP_201_CREATED
        original_count = result.json["testingUpdate"]
        result = client.put('/counters/testingUpdate')
        assert result.status_code == status.HTTP_200_OK
        new_count = result.json["testingUpdate"]
        assert original_count + 1 == new_count

    def test_get_counter(self, client):
        result = client.post('/counters/testingGet')
        assert result.status_code == status.HTTP_201_CREATED
        original_count = result.json["testingGet"]
        result = client.get('/counters/testingGet')
        assert result.status_code == status.HTTP_200_OK
        returned_count = result.json["testingGet"]
        assert original_count == returned_count

    def test_del_counter(self, client):
        counter_name = '/counters/testingDel'
        result = client.post(counter_name)
        assert result.status_code == status.HTTP_201_CREATED
        result = client.delete(counter_name)
        assert result.status_code == status.HTTP_204_NO_CONTENT
        result = client.get(counter_name)
        assert result.status_code == status.HTTP_404_NOT_FOUND

    def test_del_counter_not_present(self, client):
        counter_name = '/counters/testingDelNotPresent'
        result = client.delete(counter_name);
        assert result.status_code == status.HTTP_404_NOT_FOUND
