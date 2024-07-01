from ..common_library.Ultipro_scraper import *

ULTIPRO_OR_UKG = "UKG"
EMPLYOER_ID = "ALL1045ALLH"
JOB_BOARD_ID = "4bb296bb-0ee0-46ad-acaa-0cb594bbee0b"
COMPANY = "All-American Home Care"
UKG_EMPLOYER_DOMAIN = "aahc17"


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
