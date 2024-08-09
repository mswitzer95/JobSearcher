from ..common_library.ADP_scraper import *

C_ID = "ac19b2f4-43fe-45a4-afc9-7970e6c0a94d"
COMPANY = "Goodwill of the Finger Lakes"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(c_id=C_ID, company=COMPANY)
    return job_postings
