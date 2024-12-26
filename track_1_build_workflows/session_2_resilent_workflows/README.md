# MLB Game Analysis Pipeline

## Overview
This project contains a series of example pipelines that demonstrate how to use Prefect for scheduling, implementing error handling, data quality checks, and automated retries. Each example is an iteration of a data pipeline that fetches and analyzes MLB game statistics using the MLB Stats API.

## Topics we'll cover:
- Fetching MLB game data for specified date ranges
- Calculates game statistics including score differentials and game duration
- Implementing error handling for API failures
- Data quality checks
- Storage of results in local JSON files
- Running pipelines on a configurable schedule

## Prerequisites
- Python 3.8+
- Prefect 3.0+

## Project Contents
- `mlb_flow.py`: A basic pipeline that fetches and analyzes MLB game statistics for a specified team and date range.
- `mlb_flow_scheduled.py`: A scheduled version of the `mlb_flow.py` pipeline.
- `mlb_flow_rollback.py`: A version of the `mlb_flow.py` pipeline with error handling and data quality checks.
- `mlb_flow_retry.py`: A version of the `mlb_flow.py` pipeline with automated retries.
- `mlb_flow_exponential_retry.py`: A version of the `mlb_flow.py` pipeline with exponential backoff retries.
- `mlb_flow_delayed_retry.py`: A version of the `mlb_flow.py` pipeline with delayed retries.
- `mlb_flow_custom_retry.py`: A version of the `mlb_flow.py` pipeline with custom retry logic.
- `raw_data`: A folder for storing raw data from the MLB Stats API.
- `boxscore_analysis`: A folder for storing boxscore analysis results.
