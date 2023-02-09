"""Test the ability of the API on the User object."""
import datetime
from unittest.mock import patch

from raindropiopy.api import API, User

user = {
    "_id": 1000,
    "config": {
        "broken_level": "default",
        "font_color": "sunset",
        "font_size": 0,
        "last_collection": -1,
        "raindrops_sort": "-lastUpdate",
        "raindrops_view": "list",
    },
    "email": "mail@example.com",
    "email_MD5": "1111111111",
    "files": {
        "lastCheckPoint": "2020-01-01T02:02:02.000Z",
        "size": 10000000000,
        "used": 0,
    },
    "fullName": "test user",
    "groups": [
        {
            "collections": [
                2000,
                3000,
            ],
            "hidden": False,
            "sort": 0,
            "title": "My Collections",
        },
    ],
    "lastAction": "2020-01-01T01:01:01.000Z",
    "password": True,
    "pro": True,
    "proExpire": "2022-01-01T01:01:01.000Z",
    "provider": "twitter",
    "registered": "2020-01-02T01:1:1.0Z",
}


def test_get() -> None:
    """Test that we can get/lookup the user."""
    api = API("dummy")
    with patch("raindropiopy.api.api.OAuth2Session.request") as m:
        m.return_value.json.return_value = {"user": user}
        c = User.get(api)

        assert c.id == 1000

        assert c.email == "mail@example.com"
        assert c.email_MD5 == "1111111111"
        assert c.files.size == 10000000000
        assert c.files.used == 0
        assert c.files.lastCheckPoint == datetime.datetime(
            2020,
            1,
            1,
            2,
            2,
            2,
            tzinfo=datetime.timezone.utc,
        )
        assert c.fullName == "test user"
        assert c.groups[0].hidden is False
        assert c.groups[0].sort == 0
        assert c.groups[0].title == "My Collections"
        assert list(c.groups[0].collectionids) == [2000, 3000]
        assert c.password is True
        assert c.pro is True
        assert c.registered == datetime.datetime(
            2020,
            1,
            2,
            1,
            1,
            1,
            tzinfo=datetime.timezone.utc,
        )