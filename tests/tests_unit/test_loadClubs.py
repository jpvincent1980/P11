import json

from ... import server


def test_load_clubs():
    with open('tests/tests_unit/test_clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
    assert len(listOfClubs) == 3
    assert listOfClubs[0] == {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13"
    }
    assert listOfClubs == [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        }
    ]
