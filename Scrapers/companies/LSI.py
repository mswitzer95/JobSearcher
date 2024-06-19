from common_library.ADP_scraper import *

C_ID = "6937d324-4311-405a-8417-b583fbf6c762"
COMPANY = "LSI Solutions"
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
