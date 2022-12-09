CREATE_TABLE = [
    """
CREATE TABLE IF NOT EXISTS public.city
(
    nom character varying(60) NOT NULL,
    departement character varying(3),
    code integer,
    code_postal integer,
    loyer decimal,
    population integer,
    note decimal, 
    PRIMARY KEY (code)
);
""",
    """CREATE INDEX IF NOT EXISTS city ON city (departement)""",  # Speed up query
]

TABLE_COLUMNS = ["nom", "departement", "code", "code_postal", "loyer", "population", "note"]