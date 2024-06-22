from ..common_library.ADP_scraper import *

C_ID = "c20206a3-3c95-4ceb-b207-09e843c800d3"
COMPANY = "Lyons National Bank"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(c_id=C_ID, company=COMPANY)
    return job_postings
