from ..common_library.ADP_scraper import *

C_ID = "39c19775-5868-44f1-a8a2-c758a1dd4bbb"
COMPANY = "FIFCO"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(c_id=C_ID, company=COMPANY)
    return job_postings
