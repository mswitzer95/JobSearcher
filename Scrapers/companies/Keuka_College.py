from ..common_library.Paylocity_scraper import *

EMPLOYER_ID = "79f94d92-d2c7-407b-923b-2c8ba8a4a263"
EMPLOYER_NAME = "Keuka-College-Faculty-Staff"
COMPANY = "Keuka College"


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
