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
    """
    TestCounterEndPoints contains tests for various operations on counters, including creation, 
    updating, reading, and deletion. It verifies both successful operations and edge cases, 
    such as handling non-existent or duplicate counters.
    """


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
        """It should update a counter by incrementing its value. This test creates a counter, verifies the initial value (0), increments it by 1, and checks the updated value."""
        counter_name = 'unique_foo'

        # Step 1: Create the counter
        create_response = client.post(f'/counters/{counter_name}')
        assert create_response.status_code == status.HTTP_201_CREATED

        # Step 2: Check the initial value of the counter
        get_response = client.get(f'/counters/{counter_name}')
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json[counter_name] == 0

        # Step 3: Update the counter (increment by 1)
        update_response = client.put(f'/counters/{counter_name}')
        assert update_response.status_code == status.HTTP_200_OK

        # Step 4: Check the updated value of the counter
        get_response_after_update = client.get(f'/counters/{counter_name}')
        assert get_response_after_update.status_code == status.HTTP_200_OK
        assert get_response_after_update.json[counter_name] == 1  # Value should be incremented by 1


    def test_read_a_counter(self, client):
        """Test reading a counter after creating it. The test ensures that the counter starts with a value of 0 upon creation."""
        counter_name = 'unique_read'

        create_response = client.post(f'/counters/{counter_name}')
        assert create_response.status_code == 201  # Created

        get_response = client.get(f'/counters/{counter_name}')
        assert get_response.status_code == 200
        assert get_response.json[counter_name] == 0  # Initially, counter should be 0


    def test_get_non_existent_counter(self, client):
        """
        It should return a 404 NOT FOUND for a non-existent counter.

        This test ensures that the service handles cases where a client attempts 
        to read a counter that does not exist, returning an appropriate error message 
        and status code. This is important for ensuring that clients get meaningful feedback 
        when making invalid requests.
        """
        counter_name = 'non_existent_counter'  # Name of the counter that does not exist

        # Attempt to retrieve the non-existent counter
        response = client.get(f'/counters/{counter_name}')

        # Assert that the response status code is 404 NOT FOUND
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Assert that the response message is correct
        assert response.json == {"message": f"Counter {counter_name} not found"}


    def test_update_non_existent_counter(self, client):
        """It should return a 404 NOT FOUND for a non-existent counter"""
        counter_name = 'non_existent_counter'  # Name of the counter that does not exist

        # Attempt to update the non-existent counter
        response = client.put(f'/counters/{counter_name}')

        # Assert that the response status code is 404 NOT FOUND
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Assert that the response message is correct
        assert response.json == {"message": f"Counter {counter_name} not found"}


    def test_delete_counter(self, client):
        """It should delete an existing counter and verify that the counter is no longer retrievable (returns 404 after deletion)."""
        counter_name = 'test_counter'

        # Create the counter first
        client.post(f'/counters/{counter_name}')

        # Now delete the counter
        response = client.delete(f'/counters/{counter_name}')

        # Assert that the response status code is 204 NO CONTENT
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Assert that the counter is actually deleted
        get_response = client.get(f'/counters/{counter_name}')
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


    def test_delete_non_existent_counter(self, client):
        """It should return 404 NOT FOUND when trying to delete a non-existent counter"""
        counter_name = 'non_existent_counter'

        # Attempt to delete the non-existent counter
        response = client.delete(f'/counters/{counter_name}')

        # Assert that the response status code is 404 NOT FOUND
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Assert that the response message is correct
        assert response.json == {"message": f"Counter {counter_name} not found"}

