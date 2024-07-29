from ..common_library.Dayforce_scraper import *

EMPLOYER_NAME = "kodakalaris"
JOB_BOARD_NAME = "CANDIDATEPORTAL"
COMPANY = "Kodak Alaris"
LOCATION = "Rochester, NY, USA"
PAY_CLASS = None #1

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
        location=LOCATION,
        pay_class=PAY_CLASS)
    return job_postings
