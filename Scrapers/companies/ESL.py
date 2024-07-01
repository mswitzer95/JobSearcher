from ..common_library.Ultipro_scraper import *

ULTIPRO_OR_UKG = "Ultipro"
EMPLYOER_ID = "ESL1000ESL"
JOB_BOARD_ID = "0690c0e1-6bba-4977-83bf-9bde86c5080b"
COMPANY = "ESL"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(
        Ultipro_or_UKG=ULTIPRO_OR_UKG,
        employer_id=EMPLYOER_ID,
        job_board_id=JOB_BOARD_ID,
        company=COMPANY)
    return job_postings
