import unittest

import pandas as pd
from src.price import Price


class TestGouv(unittest.TestCase):
    def test_scrap(
        self,
    ):
        price = Price()
        priced = price.scrap(pd.DataFrame(data=[["92004"]], columns=["code"]))
        assert priced.equals(
            pd.DataFrame(data=[["92004", 20.82248488]], columns=["code", "loyer"])
        )
