from sqlalchemy import select, func, distinct
from sqlalchemy.orm import sessionmaker
import json

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT
from db_connect import get_engine

from models import Launch

def get_flight_average(session):

    sql = select(func.avg(Launch.flight_number).label("avg_flight_number"))
    return [dict(row) for row in session.execute(sql).mappings().all()]

def get_unique_rockets(session):

    sql = select(func.count(distinct(Launch.rocket)).label("unique_rockets"))
    return [dict(row) for row in session.execute(sql).mappings().all()]

def get_launches_per_year(session):

    sql = (
        select(Launch.launch_year, func.count().label("total_launches"))
        .group_by(Launch.launch_year)
        .order_by(Launch.launch_year)
    )
    return [dict(row) for row in session.execute(sql).mappings().all()]


def create_report() -> None:
    engine = get_engine(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT)

    Session = sessionmaker(bind=engine)
    with Session() as session:

        avg_flight = get_flight_average(session=session)
        unique_rockets = get_unique_rockets(session=session)
        launches_per_year = get_launches_per_year(session=session)

        results = {
            "average_flight_number": avg_flight,
            "unique_rockets": unique_rockets,
            "launches_per_year": launches_per_year,
        }

        #print(results)
        with open("report.json", "w") as f:
            json.dump(results, f, indent=4)

    engine.dispose()


if __name__ == "__main__":
    create_report()