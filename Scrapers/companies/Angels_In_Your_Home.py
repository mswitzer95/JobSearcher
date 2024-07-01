from ..common_library.Paylocity_scraper import *

EMPLOYER_ID = "31e31306-d299-4654-b1e7-39291edced51"
EMPLOYER_NAME = "Angels-In-Your-Home-LHCSA"
COMPANY = "Angels In Your Home"


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
