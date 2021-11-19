from ... import server


def test_logout():
    """
    Tests if logout view is working by checking response status code and URL
    of the redirected view.
    """
    response = server.app.test_client()
    assert response.get('/logout').status_code == 302
    assert b'target URL: <a href="/">/</a>' in response.get('logout').data
