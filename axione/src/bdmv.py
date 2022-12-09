from asyncio.log import logger
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from slugify import slugify


class Note:
    def __init__(self) -> None:
        pass

    def get_note(self, city_name, code):
        """Scrap a note from a city"""
        content = BeautifulSoup(
            requests.get(
                "https://www.bien-dans-ma-ville.fr/" + slugify(f"{city_name} {code}")
            ).text,
            "lxml",
        )
        try:
            avis_section = content.find("section", {"id": "avis"})
            total = avis_section.find("div", {"class": "total"}).text
            note = total[: total.index("/")]
            return float(note)
        except Exception as e:
            logger.error(str(e))
            return 0

    def scrap(self, city_list) -> List[Dict[str, str]]:
        """
        >>> scrap([
            {
                "nom": "Levallois-Perret",
                "code": "92044",
                "codesPostaux": [
                    "92300"
                ],
                "population": 66082
            },
            ...
        ])
        ... [
            {
                "nom": "Levallois-Perret",
                "code": "92044",
                "codesPostaux": [
                    "92300"
                ],
                "population": 66082,
                "note": 3.9
            },
            ...
        ]
        """
        logger.info(f"Scrapping notes for {len(city_list)}")
        for city in city_list:
            city.update(
                {"note": self.get_note(city_name=city["nom"], code=city["code"])}
            )

        return city_list
