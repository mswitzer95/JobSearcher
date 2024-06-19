from common_library.ADP_scraper import *

C_ID = "49287248-ffdf-4d9a-aa3c-b18302894ef0"
COMPANY = "Summit FCU"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(c_id=C_ID, company=COMPANY)
    return job_postings
