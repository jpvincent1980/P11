import json
import pytest

from ... import server

TEST_DICT = {
    "name": "Face Lift",
    "email": "johnsteed@hotmail.com",
    "points": "50",
    "competition": "Spring Festival",
    "date": "2022-03-27 10:00:00",
    "numberOfPlaces": "25",
    "bookedPlaces": "2"
}


def mock_load_clubs():
    """
    Function that retrieves the list of clubs from test_clubs.json file.

    Returns a list of dictionaries
    """
    with open('tests/tests_integration/test_clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


@pytest.fixture
def fixture_load_clubs(monkeypatch):
    """
    A fixture to replace actual list of clubs with a mock list of clubs.
    """
    monkeypatch.setattr('P11.server.clubs', mock_load_clubs())


def mock_load_competitions():
    """
    Function that retrieves the list of competitions from
    test_competitions.json file.

    Returns a list of dictionaries
    """
    with open('tests/tests_integration/test_competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


@pytest.fixture
def fixture_load_competitions(monkeypatch):
    """
    A fixture to replace actual list of competitions with a mock list of
    competitions.
    """
    monkeypatch.setattr('P11.server.competitions', mock_load_competitions())


class TestIntegration:
    """
    A class that gathers tests of the following sequence of functions:
    loadClubs
    loadCompetitions
    index
    showSummary
    book
    purchasePlaces
    displayClubsPoints
    logout
    """

    def test_load_clubs(self):
        """
        A function that tests the loading of the clubs json file.
        """
        assert len(mock_load_clubs()) == 3
        assert mock_load_clubs()[0] == {
            "name": "Face Lift",
            "email": "johnsteed@hotmail.com",
            "points": "50"
        }

    def test_load_competitions(self):
        """
        A function that tests the loading of the competitions json file.
        """
        assert len(mock_load_competitions()) == 2
        assert mock_load_competitions()[0] == {
            "name": "Spring Festival",
            "date": "2022-03-27 10:00:00",
            "numberOfPlaces": "25"
        }

    def test_index(self):
        """
        Tests if index view is working by checking response status code.
        """
        response = server.app.test_client()
        assert response.get('/').status_code == 200

    def test_show_summary(self, fixture_load_clubs, fixture_load_competitions):
        """
        Tests the access to the showSummary view with a valid email registered
        email address.
        """
        email = TEST_DICT.get("email", "alternate@hotmail.com")
        response = server.app.test_client().post('/showSummary',
                                                 data=dict(email=email))
        assert response.status_code == 200
        assert f"Welcome, {email}".encode("utf-8") in response.data

    def test_book(self, fixture_load_clubs, fixture_load_competitions):
        """
        Tests if book view is working by checking response
        status code and if the number of places displayed is correct.
        """
        response = server.app.test_client().get('/book/' +
                                                TEST_DICT['competition']
                                                + '/' +
                                                TEST_DICT['name'])
        assert response.status_code == 200
        test_places = "Places available: " + TEST_DICT["numberOfPlaces"]
        assert test_places.encode("utf-8") in response.data

    def test_success_purchase_places(self,
                                  fixture_load_clubs,
                                  fixture_load_competitions):
        """
        Tests the purchasePlaces view by checking response status code and
        remaining club points and remaining competition places.
        """
        response = server.app.test_client().post('/purchasePlaces',
                                                 data=dict(club=TEST_DICT["name"],
                                                           competition=TEST_DICT["competition"],
                                                           places=TEST_DICT["bookedPlaces"]))
        assert response.status_code == 200
        message = "Great-booking complete!"
        assert message.encode("utf-8") in response.data
        remaining_clubs_points = int(TEST_DICT["points"]) - int(TEST_DICT["bookedPlaces"])*3
        remaining_clubs_points = "Points available: " + str(remaining_clubs_points)
        assert remaining_clubs_points.encode("utf-8") in response.data
        remaining_competition_places = int(TEST_DICT["numberOfPlaces"]) - int(TEST_DICT["bookedPlaces"])
        remaining_competition_places = "Number of Places: " + str(remaining_competition_places)
        assert remaining_competition_places.encode("utf-8") in response.data

    def test_success_display_clubs_points(self, fixture_load_clubs):
        """
        Tests if Display Clubs Points view is working by checking response
        status code and if the name of the club is included in the response.
        """
        response = server.app.test_client().get('/displayClubsPoints')
        assert response.status_code == 200
        assert mock_load_clubs()[0]["name"].encode("utf-8") in response.data

    def test_logout(self):
        """
        Tests if logout view is working by checking response status code and URL
        of the redirected view.
        """
        response = server.app.test_client()
        assert response.get('/logout').status_code == 302
        assert b'target URL: <a href="/">/</a>' in response.get('logout').data
