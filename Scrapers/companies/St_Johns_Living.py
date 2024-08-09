from ..common_library.ADP_scraper import *

C_ID = "56eefb5a-c0b7-4e8b-a49f-fa69b70a577b"
COMPANY = "St. John's Senior Living & Care"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(c_id=C_ID, company=COMPANY)
    return job_postings
