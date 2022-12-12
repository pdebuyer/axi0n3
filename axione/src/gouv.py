from asyncio.log import logger
import json
from typing import Dict, List

import requests


class Gouv:
    def __init__(self) -> None:
        pass

    def get_list_communes(self, departement: str) -> List[Dict[str, str]]:
        """
        >>> get_list_communes(departement="92")
        https://geo.api.gouv.fr/departements/92/communes?fields=nom,code&format=json&geometry=centre
        [
            {
                "nom": "Antony",
                "code": "92002"
            },
            {
                "nom": "Asnières-sur-Seine",
                "code": "92004"
            },
            ...
        ]
        """
        return json.loads(
            requests.get(
                f"https://geo.api.gouv.fr/departements/{departement}"
                "/communes?fields=nom,code&format=json&geometry=centre"
            ).text
        )

    def get_communes_informations(self, commune_code: str) -> dict:
        """
        >>> get_communes_informations(commune_code="92044")
        {
            "nom": "Levallois-Perret",
            "code": "92044",
            "codesPostaux": [
                "92300"
            ],
            "population": 66082
        }
        """
        return json.loads(
            requests.get(
                f"https://geo.api.gouv.fr/communes/{commune_code}"
                "?fields=nom,code,population,codesPostaux&format=json&geometry=centre"
            ).text
        )

    def scrap(self, departement: str) -> List[Dict[str, str]]:
        """_summary_
        >>> scrap(departement="92")
        [
            {
                "nom": "Levallois-Perret",
                "code": "92044",
                "codesPostaux": [
                    "92300"
                ],
                "population": 66082
            },
            ...
        ]
        """
        try:
            list_city = self.get_list_communes(departement=departement)
            logger.info(f"Number of cities {len(list_city)}")

            for city in list_city:
                city_data = self.get_communes_informations(commune_code=city["code"])
                city_data["codesPostaux"] = city_data["codesPostaux"][0]
                city.update(city_data)

            logger.info(f"Number of cities {len(list_city)}")

            return list_city
        except Exception as e:
            logger.error("No city")
            logger.error(str(e))
            return []
