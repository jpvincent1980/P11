from ... import server
from ..fixtures import fixture_load_clubs, fixture_load_competitions, test_dict


class TestBook:
    """
    A class that gathers tests for book view.
    """
    def test_success_book(self, fixture_load_clubs, fixture_load_competitions):
        """
        Tests if book view is working by checking response
        status code and if the number of places displayed is correct.
        """
        response = server.app.test_client().get('/book/' +
                                                test_dict['competition']
                                                + '/' +
                                                test_dict['name'])
        assert response.status_code == 200
        test_places = "Places available: " + test_dict["numberOfPlaces"]
        assert test_places.encode("utf-8") in response.data

    def test_failure_book(self, fixture_load_clubs, fixture_load_competitions):
        """
        Tests if book view is working by checking response
        status code of an invalid URL path.
        """
        response = server.app.test_client().get('/book/' +
                                                "fake_competition"
                                                + '/' +
                                                test_dict['name'])
        assert response.status_code == 200
        assert b"Something went wrong-please try again" in response.data

    def test_failure_book_2(self,
                            fixture_load_clubs,
                            fixture_load_competitions):
        """
        Tests if book view is working by checking response
        status code of an invalid URL path.
        """
        response = server.app.test_client().get('/book/' +
                                                test_dict['competition']
                                                + '/' +
                                                "fake_name")
        assert response.status_code == 200
        assert b"Something went wrong-please try again" in response.data
