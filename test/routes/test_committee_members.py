"""Checks all committee members can be loaded correctly"""


def test_committee_members(client):
    roles = {
        "president",
        "vicepresident",
        "academic",
        "access",
        "computing",
        "ents",
        "ethical",
        "equalops",
        "facilities",
        "secretary",
        "services",
        "treasurer",
        "fwelfare",
        "mwelfare",
        "bme",
        "internationals",
        "lgbtq",
        "disabilities",
        "women"
    }

    for role in roles:
        response = client.get("/yourjcr/committee/{}".format(role))
        assert response.status_code == 200
