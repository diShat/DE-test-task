import os
import pandas as pd
from sqlalchemy import MetaData

from config import DATA_PROCESSED_PATH
from datetime import datetime

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT
from db_connect import get_engine

from models import Base


def init_table(engine) -> None:

    Base.metadata.create_all(engine)  # creates if not exists


def read_from_parquet(filename: str = "data.parquet", date: datetime = datetime.now()) -> pd.DataFrame:

    filepath = os.path.join(DATA_PROCESSED_PATH, date.strftime("%Y-%m-%d"), filename)
    df = pd.read_parquet(filepath, engine="fastparquet")

    return df


def write_to_table(engine, df: pd.DataFrame) -> None:
    df.to_sql("launches", engine, if_exists="append", index=False)


def load_data() -> None:
    engine = get_engine(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT)
    init_table(engine)

    df = read_from_parquet()

    write_to_table(engine, df)
    
    engine.dispose()


if __name__ == "__main__":
    load_data()