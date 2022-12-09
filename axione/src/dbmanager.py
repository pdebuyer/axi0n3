from asyncio.log import logger
from io import StringIO
from typing import List

import pandas as pd
import psycopg2.extras
import psycopg2

from .constants import CREATE_TABLE

# Database
DATABASE = {
    "database": "postgres",
    "user": "axione",
    "password": "paul",
    "host": "database",
    "port": 5432,
}


class DBManager:
    def __init__(self, db=None) -> None:
        self.db = psycopg2.connect(**DATABASE)

    def create_table(
        self,
    ):
        """Create all the tables. Only necessary to be called
        when you iniatilize the application"""
        for query in CREATE_TABLE:
            self.query(query)
        self.db.commit()

    def get_connector(self):
        """Get the connector used for the SQL queries"""
        return self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def update_table_from_extract(self, df: pd.DataFrame) -> None:
        """Update the tables with the scrapped data

        Parameters
        ----------
        df : pd.DataFrame
            dataframe containing the datas
        """
        self.add_to_table(df, table="city")

    def add_to_table(self, df: pd.DataFrame, table="city"):
        """Update a single table"""
        logger.info(f"Update table {table} with {df.shape[0]} new lines")
        # Bruteforcing: case of duplicate - Not optimal -
        for line_number in range(df.shape[0]):
            try:
                # Save in a file stored in a memory
                temp_file = StringIO()
                df.iloc[[line_number]].to_csv(
                    temp_file, header=None, sep=",", index=False
                )
                temp_file.seek(0)

                # Update from dataframe
                cursor = self.get_connector()
                cursor.copy_from(temp_file, table, null="", sep=",", columns=df.columns)
                # Save the database
                self.db.commit()

            except Exception as e:
                cursor.execute("ROLLBACK")
                logger.debug(str(e))

    def query(self, query: str):
        """Execute a SQL query"""
        logger.info("Executing a query")
        cursor = self.get_connector()
        cursor.execute(query)
        return cursor

    def check_if_scrapped(self, departement: str) -> bool:
        """Check if a departement is scrapped"""
        cursor = self.query(
            f"""
            SELECT departement 
            FROM public.city 
            WHERE departement='{departement}' limit 1"""
        )
        return len(cursor.fetchall()) > 0

    def get_cities(self, departement: str) -> List:
        """Get the informations relatives to city"""
        return self.query(
            f"""
            SELECT * 
            FROM public.city
            WHERE departement='{departement}'
        """
        ).fetchall()
