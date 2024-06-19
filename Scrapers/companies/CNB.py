from common_library.ADP_scraper import *

C_ID = "2e4e5521-e8a5-4572-9ffd-3c8e382ee6f2"
COMPANY = "Canadaigua National Bank & Trust"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(c_id=C_ID, company=COMPANY)
    return job_postings
