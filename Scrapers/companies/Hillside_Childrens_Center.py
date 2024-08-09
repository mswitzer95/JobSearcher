from ..common_library.Oracle_scraper import *

BASE_DOMAIN = "https://ebrf.fa.us2.oraclecloud.com/"
SITE_NUMBER = "CX_1"
LOCATION_ID = ""
COMPANY = "Hillside Children's Center"


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
