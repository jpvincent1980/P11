from ... import server
from ..fixtures import mock_load_clubs, fixture_load_clubs


class TestDisplayClubsPoints:
    """
    A class that gathers tests for displayClubsPoints view.
    """
    def test_success_display_clubs_points(self, fixture_load_clubs):
        """
        Tests if Display Clubs Points view is working by checking response
        status code and if the name of the club is included in the response.
        """
        response = server.app.test_client().get('/displayClubsPoints')
        assert response.status_code == 200
        assert mock_load_clubs()[0]["name"].encode("utf-8") in response.data
