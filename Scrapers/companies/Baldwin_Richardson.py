from ..common_library.ADP_scraper import *
import logging

C_ID = "45a38de5-f641-48c7-8a2a-89642281328d"
COMPANY = "Baldwin Richardson Foods"
USER_QUERY = "NY"
LOGGER = logging.getLogger()


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
