import pandas as pd


class Price:
    def __init__(self) -> None:
        pass

    def scrap(self, city_dataframe: pd.DataFrame) -> pd.DataFrame:
        data = pd.read_csv(
            "axione/data/indicateurs-loyers-appartements.csv",
            sep=";",
            usecols=["INSEE", "loypredm2"],
        ).rename(columns={"INSEE": "code", "loypredm2": "loyer"})
        return city_dataframe.merge(data, on=["code"], how="left")
