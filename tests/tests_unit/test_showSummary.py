from ... import server
from ..fixtures import fixture_load_clubs, fixture_load_competitions, test_dict


class TestShowSummary:
    """
    A class that gathers tests for showSummary view.
    """
    def test_success_show_summary(self,
                                  fixture_load_clubs,
                                  fixture_load_competitions):
        """
        Tests the access to the showSummary view with a valid email registered
        email address.
        """
        email = test_dict.get("email", "alternate@hotmail.com")
        response = server.app.test_client().post('/showSummary',
                                                 data=dict(email=email))
        assert response.status_code == 200
        assert f"Welcome, {email}".encode("utf-8") in response.data

    def test_failure_show_summary(self):
        """
        Tests the access to the showSummary view with an unregistered email
        address. User is redirected to the login page if email address is not
        registered. (hence status code == 302)
        """
        response = server.app.test_client()
        assert response.post('/showSummary',
                             data=dict(email="unknown@address.com")).status_code == 302
