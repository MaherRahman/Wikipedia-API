# Import pytest and requests libraries
import pytest
import requests

# Define the base URL for the flask application
base_url = "http://127.0.0.1:5000"

# Define a fixture to create a session object that can be reused across tests
@pytest.fixture(scope="module")
def session():
    return requests.Session()

# Test the home route
def test_home(session):
    response = session.get(base_url + "/")
    assert response.status_code == 200

# Test the most-viewed-week route with valid parameters
def test_most_viewed_week_valid(session):
    response = session.get(base_url + "/most-viewed/2016/10/02")
    assert response.status_code == 200
    
    data = response.json()
    
    firstarticle = data[0]
    assert firstarticle["article"] == "Main_Page"
    assert firstarticle["views"] == 187456507    
    
    thirdarticle = data[2]
    assert thirdarticle["article"] == "Anterior_interventricular_branch_of_left_coronary_artery"
    assert thirdarticle["views"] == 3970826 

# Test the most-viewed-week route with invalid parameters
def test_most_viewed_week_invalid(session):
    response = session.get(base_url + "/most-viewed/2023/13/01")
    assert response.status_code == 404
    assert "Invalid Month" in response.text

# Test the most-viewed route with valid parameters
def test_most_viewed_valid(session):
    response = session.get(base_url + "/most-viewed/2023/01")
    data = response.json()
    
    firstarticle = data[0]
    assert firstarticle["article"] == "Main_Page"
    assert firstarticle["views"] == 153563201    
    
    sixtharticle = data[5]
    assert sixtharticle["article"] == "Avatar:_The_Way_of_Water"
    assert sixtharticle["views"] == 6522721 

# Test the most-viewed route with invalid parameters
def test_most_viewed_invalid(session):
    response = session.get(base_url + "/most-viewed/2024/12")
    assert response.status_code == 404
    assert "Invalid Year" in response.text

# Test the view-count-week route with valid parameters
def test_view_count_week_valid(session):
    response = session.get(base_url + "/view-count/Barack_Obama/2016/1")
    assert response.status_code == 200
    assert response.json() == 1259488

# Test the view-count-week route with invalid parameters
def test_view_count_week_invalid(session):
    response = session.get(base_url + "/view-count/Barack_Obama/2016/1/5")
    assert response.status_code == 404
    assert "Invalid Week" in response.text

# Test the view-count route with valid parameters
def test_view_count_valid(session):
    response = session.get(base_url + "/view-count/Barack_Obama/2016/1/2")
    assert response.status_code == 200
    assert response.json() == 60742

# Test the view-count route with invalid parameters
def test_view_count_invalid(session):
    response = session.get(base_url + "/view-count/Barack_Obama/2016/13")
    assert response.status_code == 404
    assert "Invalid Month" in response.text

# Test the most-viewed-day route with valid parameters
def test_most_viewed_day_valid(session):
    response = session.get(base_url + "/most-viewed-day/Albert_Einstein/2015/10")
    assert response.status_code == 200
    assert response.json() == 29

# Test the most-viewed-day route with invalid parameters
def test_most_viewed_day_invalid(session):
    response = session.get(base_url + "/most-viewed-day/Albert_Einstein/2024/10")
    assert response.status_code == 404
    assert "Invalid Year" in response.text