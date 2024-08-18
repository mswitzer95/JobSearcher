from ..common_library.ADP_scraper import *

C_ID = "0a5266d0-2e2e-48d3-a5a2-665ac2a11a57"
COMPANY = "Arnold Magnetics"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(c_id=C_ID, company=COMPANY)
    return job_postings
