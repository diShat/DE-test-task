from sqlalchemy import create_engine, text
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT


def get_engine(user, password, host, dbname, port=5432):

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

    return create_engine(url)


if __name__ == "__main__":

    #engine = get_engine(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT)

    ## Quick check
    #with engine.connect() as conn:
    #    print(conn.execute(text("SELECT current_user, current_database();")).fetchall())

    #engine.dispose()

    pass