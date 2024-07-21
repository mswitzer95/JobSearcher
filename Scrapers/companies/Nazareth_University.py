from ..common_library.PeopleAdmin_scraper import *

DOMAIN_NAME = "https://jobs.naz.edu/"
COMPANY = "Nazareth University"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(
        domain_name=DOMAIN_NAME,
        company=COMPANY)
    return job_postings
