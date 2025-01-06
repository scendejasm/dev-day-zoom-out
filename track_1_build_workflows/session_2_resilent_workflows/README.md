# Track 1, Session 2: Schedule workflows and make them resilient

## Overview
This project contains a series of example pipelines that demonstrate how to use Prefect implementing error handling, data quality checks, and automated retries. Each example is an iteration of a data pipeline that fetches and analyzes MLB game statistics using the MLB Stats API. Specifically, we'll be looking at the correlation between the score differential and the game duration.

## Topics we'll cover:
- Running pipelines on a configurable schedule
- Automatic retries and implementing custom error handling for API failures
- Prefect transactions, rollbacks, and data quality checks
- Storage of results in local JSON files, MotherDuck, and S3


## Project Contents
- `mlb_flow.py`: A basic pipeline that fetches and analyzes MLB game statistics for a specified team and date range.
- `mlb_flow_retry_1.py`: A version of the `mlb_flow.py` pipeline with automated retries.
- `mlb_flow_delayed_retry_2.py`: A version of the `mlb_flow.py` pipeline with delayed retries.
- `mlb_flow_exponential_retry_3.py`: A version of the `mlb_flow.py` pipeline with exponential backoff retries.
- `mlb_flow_custom_retry_4.py`: A version of the `mlb_flow.py` pipeline with custom retry logic.
- `mlb_flow_rollback_5.py`: A version of the `mlb_flow.py` pipeline with error handling and data quality checks.
- `mlb_flow_scheduled_6.py`: A scheduled version of the `mlb_flow.py` pipeline.
- `raw_data`: A folder for storing raw data from the MLB Stats API.
- `boxscore_analysis`: A folder for storing boxscore analysis results.
- `boxscore_parquet`: A folder for storing boxscore analysis results in parquet format.

