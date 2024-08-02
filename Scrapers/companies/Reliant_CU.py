from ..common_library.Paylocity_scraper import *

EMPLOYER_ID = "8dda6878-ada5-4ef2-85ec-08f3d8f3418f"
EMPLOYER_NAME = "Reliant-Community-Credit-Union"
COMPANY = "Reliant Credit Union"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(
        employer_id=EMPLOYER_ID,
        employer_name=EMPLOYER_NAME,
        company=COMPANY)
    return job_postings
