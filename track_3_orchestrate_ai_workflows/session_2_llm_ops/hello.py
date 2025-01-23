# Import required libraries
import asyncio
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from prefect.concurrency.asyncio import concurrency, rate_limit
from prefect import flow, task
import httpx

# Load environment variables (e.g. OPENAI_API_KEY)
# TODO: Add your OPENAI_API_KEY to the .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Sample resume text and company to search jobs for
resume = "Product Manager with 8 years of experience in ML, AI, and DevTools."
slugs = ["stripe", "flatironhealth"]

# Define the structure for job matching results using Pydantic
class Job(BaseModel):
    is_a_fit: bool = Field(
        description="""
        Whether the job is a fit for the candidate.
        """
    )

# Function to analyze if a job posting matches the resume using OpenAI
@task
async def transform(data: str) -> Job | None:
    await rate_limit("openai-rate-limited-request")
    async with concurrency("tokens", occupy=16384):
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Candidate resume: {resume}"},
                {"role": "user", "content": data},
            ],
            max_tokens=16384,
            response_format=Job,
        )
        return response.choices[0].message.parsed

# Function to fetch job postings and analyze them in parallel
@flow
# Function to fetch job postings and analyze them in parallel
async def load() -> list[Job | None] | None:
    results: list[Job | None] = []
    async with httpx.AsyncClient() as client:
        # For each company in our list
        for slug in slugs:
            # Fetch jobs from Greenhouse's API
            response = await client.get(
                f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
            )
            data = response.json()
            # Create tasks to analyze first 3 jobs
            coros = [transform(job["content"]) for job in data["jobs"][:3]]
            # Run analysis in parallel and return results
            results.extend(await asyncio.gather(*coros))
    return results

if __name__ == "__main__":
    asyncio.run(load())
