from ... import server


def test_load_competitions():
    assert len(server.loadCompetitions()) == 2
    assert server.loadCompetitions()[0] == {
            "name": "Spring Festival",
            "date": "2022-03-27 10:00:00",
            "numberOfPlaces": "25"
        }
    assert server.loadCompetitions() == [
        {
            "name": "Spring Festival",
            "date": "2022-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]