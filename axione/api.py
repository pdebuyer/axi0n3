from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .src.city import City
from .src.dbmanager import DBManager

DBManager().create_table()
app = FastAPI()

RESULTS_COLUMS = ["loyer", "note", "nom", "code_postal", "population"]

import logging

logging.basicConfig(
    format="%(levelname)s: %(asctime)s [%(funcName)s @ %(filename)s:%(lineno)s] %(message)s",
    level=logging.INFO,
)


@app.get("/")
def read_root():
    """Check health"""
    return {"Hello": "World"}


@app.get("/best_city")
def get_cities(departement: str, max_loyer: str, surface: str):
    """Asked API"""
    city = City()
    try:
        return JSONResponse(
            city.get_list(
                departement=departement,
                max_loyer=float(max_loyer),
                surface=float(surface),
            )
            .sort_values(by="note", ascending=False)[RESULTS_COLUMS]
            .to_dict("records")
        )
    except Exception as e:
        return JSONResponse(
            f"Server encountered the following issue {str(e)}", status_code=500
        )


@app.get("/rollback")
def rollback():
    """If needed (never but in case)"""
    DBManager().get_connector().execute("ROLLBACK")
    return {"roll": "back"}
