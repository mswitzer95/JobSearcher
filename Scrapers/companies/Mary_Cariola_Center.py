from ..common_library.Ultipro_scraper import *

ULTIPRO_OR_UKG = "Ultipro"
EMPLYOER_ID = "MAR1003MCCC"
JOB_BOARD_ID = "48acbdef-c2f0-4006-bc45-6a9200919be4"
COMPANY = "Mary Cariola Center"


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
