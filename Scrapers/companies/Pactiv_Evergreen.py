from ..common_library.iCIMS_scraper import *

DOMAIN_NAME = "https://careers-pactiv-evergreen.icims.com/"
COMPANY = "Pactiv Evergreen"
LOCATIONS = ["-12816-Canandaigua"]


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
