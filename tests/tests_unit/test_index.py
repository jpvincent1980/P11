from ... import server


def test_index():
    """
    Tests if index view is working by checking response status code.
    """
    response = server.app.test_client()
    assert response.get('/').status_code == 200
