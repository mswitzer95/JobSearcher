from ..common_library.Paylocity_scraper import *

EMPLOYER_ID = "58f29f39-7f50-4695-8aef-de30a5c1a26b"
EMPLOYER_NAME = "JN-White-Designs-Screenprint-INC"
COMPANY = "JN White"


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
