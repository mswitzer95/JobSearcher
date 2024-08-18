from ..common_library.ADP_scraper import *

C_ID = "39df1cae-144e-4200-bb28-c918ae34506b"
COMPANY = "Evans Bank"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(c_id=C_ID, company=COMPANY)
    return job_postings
