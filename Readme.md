# ETL Script Test Task

Done by Diana Shatkovska

## Overview

This repository contains an ETL (Extract, Transform, Load) pipeline
developed as part of a test task.
The pipeline demonstrates: 
- Extracting data from an external API.
- Transforming the raw data into a structured format.
- Loading the processed data into a PostgreSQL database.
- Making simple queries to the database and creating a report.

Additional tools used include **Docker Compose** for containerized
Postgres, a **Makefile** for streamlined commands, and an **Airflow
DAG** prepared (but not enabled) for orchestration.

------------------------------------------------------------------------

### API Used

- **API Source**: [SpaceX v4 REST API](https://github.com/r-spacex/SpaceX-API/tree/master/docs/launches/v4)  
- **Endpoint Used**: [`https://api.spacexdata.com/v4/launches/past`](https://api.spacexdata.com/v4/launches/past)  
- **Authentication**: Not required  

------------------------------------------------------------------------

### Data Selected
For this ETL pipeline, I focused on a curated subset of fields relevant for analysis and reporting.  
The columns extracted from each launch record are:

- `id` → Unique launch identifier  
- `name` → Mission name  
- `date_utc` → Launch date in UTC  
- `date_precision` → Granularity of the launch date (e.g., hour, day, month)  
- `success` → Boolean flag indicating mission success  
- `upcoming` → Boolean flag indicating whether launch is future/upcoming  
- `tbd` → Boolean flag indicating if the launch date is yet to be determined  
- `rocket` → Reference ID of the rocket used  
- `cores[0].core` → Core ID used in the launch, renamed as `core`
- `cores[0].flight` → Number of flights completed by this core, renamed as `core_flight`
- `cores[0].landing_success` → Boolean indicating whether the core landing was successful, renamed as `core_landing_success`
- `cores[0].landing_type` → Type of landing attempted (e.g., RTLS, ASDS), renamed as `core_landing_type`
- `links.wikipedia` → Wikipedia link with mission details, renamed as `links_wikipedia`
- `details` → Free-text description of the launch 

Added colums:
- `launch_year` → Year of the launch
- `core_reused` → Boolean indicating whether the core was reused.

> These fields are demonstrated and explored in the accompanying Jupyter Notebook (`exploration.ipynb`) before being used in the ETL pipeline.

------------------------------------------------------------------------

## ETL Scripts

The pipeline is divided into four main steps:

1.  **Extract**
    -   Script: `src/fetch_api_script.py`
    -   Function: Calls the API, retrieves raw JSON, saves raw data to designated directory.
2.  **Transform**
    -   Script: `src/transform_data_script.py`
    -   Function: Normalizes, cleans data and converts it to types. Saves clean data into designated directory.
3.  **Load**
    -   Script: `src/load_to_db_script.py`
    -   Function: Loads transformed data into PostgreSQL.
3.  **Report**
    -   Script: `src/sql_reports_script.py`
    -   Function: Performs 3 simple sql queries on datatable for demonstration and creates a report.json file.

All scripts can be run individually or orchestrated via Makefile (see the section below).

------------------------------------------------------------------------

## PostgreSQL & Docker Compose

-   A `docker-compose.yml` file is included to spin up a local
    **Postgres database**.
-   Database credentials, ports, and volumes are configured for
    persistence.
-   Run `docker-compose up -d` to start the service (or use "make up" command).

------------------------------------------------------------------------

## Makefile

The **Makefile** provides shortcuts for common operations: 
- `make up` → Start Postgres via Docker Compose.
- `make down` → Stop containers.
- `make extract` → Run extract script.
- `make transform` → Run transform script.
- `make load` → Run load script.
- `make etl` → Run the full pipeline in order (without creating report).
- `make report` → Run report script.
- `make dump` → Perform database dump.
- `make requirements` → Install the requirements.

------------------------------------------------------------------------

## Airflow DAG (Optional)

An **Airflow DAG file** (`etl_dag.py`) is included in the repo but not
deployed.
It demonstrates how this ETL process could be scheduled and monitored in
a production-like environment.

------------------------------------------------------------------------

## How to Run

1.  Clone this repository.

2.  Rename .env.example back to .env .

3.  Start Docker with Postgres:

    ``` bash
    make up
    ```

4.  Run the ETL pipeline:

    ``` bash
    make etl
    ```

5.  Create sql report:

    ``` bash
    make report
    ```

------------------------------------------------------------------------

## Repository Structure

        .
    ├── Makefile
    ├── Readme.md
    ├── data
    │   ├── processed
    │   │   └── 2025-09-18
    │   │       └── data.parquet
    │   └── raw
    │       └── 2025-09-18
    │           └── responce.json
    ├── docker-compose.yaml
    ├── dump.sql
    ├── report.json
    ├── requirements.txt
    ├── screenshots
    │   ├── database_working.png
    │   ├── extract_results.png
    │   └── transform_results.png
    └── src
        ├── airflow
        │   └── etl_dag.py
        ├── config.py
        ├── data_exploration
        │   └── data_exploration.ipynb
        ├── db_connect.py
        ├── fetch_api_script.py
        ├── load_to_db_script.py
        ├── models.py
        ├── sql_reports_script.py
        └── transform_data_script.py

12 directories, 23 files

------------------------------------------------------------------------

## Notes

-   This project is a simplified ETL demonstration and is not
    production-ready.
-   Error handling and logging are minimal due to lack of time for refactoring (I'm sorry).
-   The Airflow DAG is illustrative and not required to run the
    pipeline, instead use "make etl" command.
