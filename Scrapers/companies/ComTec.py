from ..common_library.Paylocity_scraper import *

EMPLOYER_ID = "c1fa4ec5-bd20-41ac-a03e-4b7b19eeb8ac"
EMPLOYER_NAME = "ComTec-Solutions"
COMPANY = "ComTec Solutions"
LOCATION = "ComTec NY Headquarters"


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
        company=COMPANY,
        location=LOCATION)
    return job_postings
