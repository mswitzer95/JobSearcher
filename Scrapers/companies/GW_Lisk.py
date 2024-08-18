from ..common_library.iCIMS_scraper import *

DOMAIN_NAME = "https://uscareers-gwlisk.icims.com/"
COMPANY = "GW Lisk"
LOCATIONS = []


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(
        domain_name=DOMAIN_NAME,
        company=COMPANY,
        locations=LOCATIONS)
    return job_postings
