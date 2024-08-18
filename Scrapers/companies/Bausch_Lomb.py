from ..common_library.SuccessFactors_scraper import *

DOMAIN_NAME = "https://careers.bauschlomb.com/"
COMPANY = "Bausch + Lomb"
LOCATION = "US-NY-Rochester"


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
        location=LOCATION)
    return job_postings
