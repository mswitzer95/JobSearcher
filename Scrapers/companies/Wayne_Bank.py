from ..common_library.ADP_scraper import *

C_ID = "9d678dd0-7456-4530-ab98-c41a8f5f69bd"
COMPANY = "Wayne Bank"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(c_id=C_ID, company=COMPANY)
    return job_postings
