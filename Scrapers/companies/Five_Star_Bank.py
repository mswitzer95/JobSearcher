from ..common_library.ADP_scraper import *

C_ID = "d041dd25-4cbf-4fcd-bf77-ecd856f31f0f"
COMPANY = "Five Star Bank"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(c_id=C_ID, company=COMPANY)
    return job_postings
