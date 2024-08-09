from ..common_library.Ultipro_scraper import *

ULTIPRO_OR_UKG = "Ultipro"
EMPLYOER_ID = "JEW1004JSL"
JOB_BOARD_ID = "5bac926e-c267-439c-a990-f7617b3b0d2c"
COMPANY = "Jewish Senior Life"


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
