from common_library.ADP_scraper import *

C_ID = "3e17567d-22fe-47cf-a1bf-ff02192fad79"
COMPANY = "LiDestri"
USER_QUERY = "NY"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(
        c_id=C_ID, company=COMPANY, user_query=USER_QUERY)
    return job_postings
