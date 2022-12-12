from asyncio.log import logger
from typing import List

import pandas as pd

from .bdmv import Note
from .dbmanager import DBManager
from .gouv import Gouv
from .price import Price

from .constants import TABLE_COLUMNS


class City:
    def __init__(self) -> None:
        pass

    def get_list(
        self, surface: float, departement: str, max_loyer: float
    ) -> pd.DataFrame:
        """Get the list cities"""
        db = DBManager()

        # Check if scrapped
        if not db.check_if_scrapped(departement):
            logger.info("Scrap the data")
            self.scrap(departement=departement)

        # Get data
        logger.info("Get the data")
        data = pd.DataFrame(
            db.get_cities(departement=departement),
            columns=TABLE_COLUMNS,
        )
        data["loyer"] = pd.to_numeric(data["loyer"])

        # Get results
        return data[data["loyer"] * surface < max_loyer]

    def scrap(self, departement: str) -> List[str]:
        """Scrap data for a given departement"""
        # Scrap data
        logger.info("Scrap gouv")
        city_informations = Gouv().scrap(departement)
        if not city_informations:
            return
        logger.info("Scrap Notes Bien dans ma ville")
        cities_with_notes = Note().scrap(city_informations)
        logger.info("Scrap Prices")
        cities_with_price = Price().scrap(pd.DataFrame.from_records(cities_with_notes))

        cities_with_price["departement"] = departement
        # Save it
        db = DBManager()
        db.add_to_table(
            cities_with_price.rename(columns={"codesPostaux": "code_postal"}),
            table="city",
        )
