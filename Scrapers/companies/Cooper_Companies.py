from ..common_library.Oracle_scraper import *

BASE_DOMAIN = "https://hcjy.fa.us2.oraclecloud.com/"
SITE_NUMBER = "CX_1"
LOCATION_ID = "300000200168003"
COMPANY = "Cooper Companies"


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
