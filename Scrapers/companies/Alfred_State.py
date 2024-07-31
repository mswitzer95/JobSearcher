from ..common_library.Interview_Exchange_scraper import *

DOMAIN_PREFIX = "alfredstate"
COMPANY_ID = "481"
COMPANY = "Alfred State"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(
        domain_prefix=DOMAIN_PREFIX,
        company_id=COMPANY_ID,
        company=COMPANY)
    return job_postings
