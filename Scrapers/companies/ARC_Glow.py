from ..common_library.Dayforce_scraper import *

EMPLOYER_NAME = "arcnewyork"
JOB_BOARD_NAME = "ARCGLOW"
COMPANY = "ARC Glow"
PAY_CLASS = 1

async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(
        employer_name=EMPLOYER_NAME,
        job_board_name=JOB_BOARD_NAME,
        company=COMPANY,
        pay_class=PAY_CLASS)
    return job_postings
