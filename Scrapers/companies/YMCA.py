from ..common_library.Paylocity_scraper import *

EMPLOYER_ID = "e154b3f6-ff4c-4452-9e25-cf488f098288"
EMPLOYER_NAME = "YOUNG-MENS-CHRISTIAN-ASSOCIATION-OF-ROCHESTER"
COMPANY = "YMCA"


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
