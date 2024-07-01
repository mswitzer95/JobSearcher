from ..common_library.Ultipro_scraper import *

ULTIPRO_OR_UKG = "Ultipro"
EMPLYOER_ID = "FFT1000THM"
JOB_BOARD_ID = "a6bf8070-d222-4b6c-bd1f-330f8351d595"
COMPANY = "Thompson Health"


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
