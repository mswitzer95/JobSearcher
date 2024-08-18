from ..common_library.Paylocity_scraper import *

EMPLOYER_ID = "2abac3c6-4f51-4bd8-bbf7-16ec650b875f"
EMPLOYER_NAME = "Quality-Vision-International-Inc"
COMPANY = "Quality Vision International"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(
        employer_id=EMPLOYER_ID,
        employer_name=EMPLOYER_NAME,
        company=COMPANY)
    return job_postings
