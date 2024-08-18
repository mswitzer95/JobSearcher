from ..common_library.ADP_scraper import *

C_ID = "caf30e6e-18e7-4242-ab75-1f23025a2aa8"
COMPANY = "Rochester Precision Optics"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(c_id=C_ID, company=COMPANY)
    return job_postings
