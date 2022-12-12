import json
import unittest

import requests_mock
from src.gouv import Gouv


@requests_mock.Mocker()
class TestGouv(unittest.TestCase):
    def test_scrap(self, mocker):
        gouv = Gouv()
        data = json.dumps(
            [
                {"nom": "Antony", "code": "92002"},
            ]
        )
        mocker.get(
            "https://geo.api.gouv.fr/departements/92/communes?fields=nom,code&format=json&geometry=centre",
            text=data,
            status_code=200,
        )

        data = json.dumps(
            {
                "nom": "Antony",
                "code": "92002",
                "codesPostaux": ["92000"],
                "population": 1000,
            }
        )
        mocker.get(
            f"https://geo.api.gouv.fr/communes/92002?fields=nom,code,population,codesPostaux&format=json&geometry=centre",
            text=data,
            status_code=200,
        )

        results = gouv.scrap("92")

        assert results == [
            {
                "nom": "Antony",
                "code": "92002",
                "codesPostaux": "92000",
                "population": 1000,
            },
        ]
