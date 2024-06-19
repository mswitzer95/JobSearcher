from common_library.ADP_scraper import *

C_ID = "3412d63d-3eba-4d9f-93f9-621ab0a2ca92"
COMPANY = "Cobblestone Capital"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(c_id=C_ID, company=COMPANY)
    return job_postings
