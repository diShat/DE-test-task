import os
import logging
import pandas as pd

from datetime import datetime
import json

from config import DATA_RAW_PATH, DATA_PROCESSED_PATH


def get_raw_data(filename: str = "responce.json", date: datetime = datetime.now()) -> list[dict]:

    filepath = os.path.join(DATA_RAW_PATH, date.strftime("%Y-%m-%d"), filename)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def clean_data(data: list[dict]) -> pd.DataFrame:

    # exploding multi-leveled json to get desired columns
    df = pd.json_normalize(data, 
                                    record_path=["cores"],
                                    meta=["id", "name", "date_utc", 
                                          "date_precision", "success", "upcoming", "tbd",
                                          "rocket", ["links", "wikipedia"], "details"
                                          ])

    # filter out not needed columns from exploded "cores" list
    cols_new = ["id", "name", "date_utc", "date_precision", "success", 
                "upcoming", "tbd", "rocket", "core", "flight", "landing_success", "landing_type", 
                "links.wikipedia","details"]
    
    df = df[cols_new]

    # renaming 
    df = df.rename(columns={"flight": "core_flight", 
                            "landing_success": "core_landing_success", 
                            "landing_type": "core_landing_type",
                            "links.wikipedia": "links_wikipedia"
                            })
    
    # remove launches with more than 1 core (decided during exploration)
    # count number of cores per launch id
    core_counts_pd = df.groupby("id")["core"].count()

    # keep only single-core launches
    single_core_ids = core_counts_pd[core_counts_pd == 1].index
    df = df[df["id"].isin(single_core_ids)].copy()

    # resolving null values in rest of columns
    df["success"] = df["success"].astype("boolean").fillna(False)

    df["core_landing_success"] = df["core_landing_success"].astype("boolean").fillna(False)
    df["core_landing_type"] = df["core_landing_type"].fillna("Expendable")
    
    df["links_wikipedia"] = df["links_wikipedia"].fillna("No link")
    df["details"] = df["details"].fillna("No details available")

    # add some calculated fields
    df["launch_year"] = pd.to_datetime(df["date_utc"]).dt.year
    df["core_reused"] = df["core_flight"] > 1

    # convert all types
    df = df.convert_dtypes()    # better idea to match types specifically, to improve consistency for each etl run
    df["date_utc"] = pd.to_datetime(df["date_utc"], utc=True, errors="coerce")

    return df


def load_processed_data(df: pd.DataFrame, filename: str = "data.parquet", date: datetime = datetime.now()) -> None:

    filepath = os.path.join(DATA_PROCESSED_PATH, date.strftime("%Y-%m-%d"), filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    df.to_parquet(filepath, engine="fastparquet", index=False)


def transform_data() -> None:
    df = clean_data(get_raw_data())
    load_processed_data(df)


if __name__ == "__main__":
    transform_data()