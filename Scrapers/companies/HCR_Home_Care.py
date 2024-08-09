from ..common_library.ADP_scraper import *

C_ID = "74015a75-000a-4ccd-a4fd-5b28c18a4cdf"
COMPANY = "HCR Home Care"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(c_id=C_ID, company=COMPANY)
    return job_postings
