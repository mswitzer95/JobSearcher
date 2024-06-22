from ..common_library.ADP_scraper import *

C_ID = "0dfe1cd9-a147-4cda-846c-b9a9083395e6"
COMPANY = "Optimax Systems"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(c_id=C_ID, company=COMPANY)
    return job_postings
