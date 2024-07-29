from ..common_library.Oracle_scraper import *

BASE_DOMAIN = "https://jpmc.fa.oraclecloud.com/"
SITE_NUMBER = "CX_1002"
LOCATION_ID = "300000020690158"
COMPANY = "JPMorgan/Chase"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(
        base_domain=BASE_DOMAIN,
        site_number=SITE_NUMBER,
        location_id=LOCATION_ID,
        company=COMPANY)
    return job_postings
