from ... import server


def test_load_clubs():
    assert len(server.loadClubs()) == 3
    assert server.loadClubs()[0] == {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13"
    }
    assert server.loadClubs() == [
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
