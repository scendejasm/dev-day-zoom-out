# LLM Job Matching Application

This application demonstrates an AI-powered job matching system using OpenAI's GPT models and Prefect for workflow orchestration. It analyzes job postings from multiple companies and determines if they match a candidate's resume.

## Features

- Asynchronous job posting retrieval from Greenhouse's API
- Parallel processing of job analyses using OpenAI's GPT models
- Rate limiting and concurrency management with Prefect
- Structured data handling with Pydantic models

## Prerequisites

- Python 3.12 or higher
- OpenAI API key
- Required Python packages (see `pyproject.toml`)

## Setup

1. Clone the repository
2. Create a `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```
   uv venv
   uv pip install -e .
   ```

## How It Works

1. The application starts with a sample resume and a list of company slugs (currently Stripe and Flatiron Health)
2. For each company:
   - Fetches job postings from Greenhouse's API
   - Analyzes the first 3 job postings using GPT-4
   - Determines if each job is a good fit for the candidate

## Key Components

- `Job` class: Pydantic model defining the structure for job matching results
- `transform()`: Task that analyzes job postings using OpenAI
- `load()`: Main flow that orchestrates the job fetching and analysis process

## Usage

Run the application:
```
uv run hello.py
```

This will execute the `load()` flow, which fetches job postings, analyzes them, and outputs the results.
