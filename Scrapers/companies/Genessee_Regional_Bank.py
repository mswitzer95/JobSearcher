from ..common_library.Ultipro_scraper import *

ULTIPRO_OR_UKG = "UKG"
EMPLYOER_ID = "GEN1500GNRB"
JOB_BOARD_ID = "1f082171-3b2f-4eb9-909d-14fc8bcb72b1"
COMPANY = "Genessee Regional Bank"
UKG_EMPLOYER_DOMAIN = "grbbank"


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
        company=COMPANY,
        UKG_employer_domain=UKG_EMPLOYER_DOMAIN)
    return job_postings
