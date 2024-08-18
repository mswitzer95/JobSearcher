from ..common_library.Paylocity_scraper import *

EMPLOYER_ID = "f5c457e3-55c9-4396-94e0-5adf373b1d9d"
EMPLOYER_NAME = ""
COMPANY = "Episcopal Senior Life Communities"


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
