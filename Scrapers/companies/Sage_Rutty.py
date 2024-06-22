from ..common_library.ADP_scraper import *

C_ID = "2fcbcca3-5106-4e10-ac7b-3567590a02bd"
COMPANY = "Sage Rutty"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(c_id=C_ID, company=COMPANY)
    return job_postings
