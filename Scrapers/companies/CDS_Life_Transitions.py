from ..common_library.ADP_scraper import *

C_ID = "58870110-bb97-40a7-82d8-456191a146d9"
COMPANY = "CDS Life Transitions"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(c_id=C_ID, company=COMPANY)
    return job_postings
