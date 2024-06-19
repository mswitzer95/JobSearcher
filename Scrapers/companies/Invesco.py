from common_library.Workday_scraper import *

WORKDAY_EMPLOYER_NAME = "Invesco"
CAREER_SITE_NAME = "IVZ"
COMPANY = "Invesco"
WORKDAY_VERSION = "wd1"
APPLIED_FACETS = {
    # Finance, investments, and investment research job families
    "jobFamilyGroup": [
        "97a56ab3ad0b1018c66825ed807b0002",
        "97a56ab3ad0b1018c66824ba54520002",
        "97a56ab3ad0b1018c668241fbc1b0000"
    ]
}
SEARCH_TEXT = "New+York"


async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    
    job_postings = await get_job_postings(
        Workday_employer_name=WORKDAY_EMPLOYER_NAME,
        career_site_name=CAREER_SITE_NAME,
        company=COMPANY,
        Workday_version=WORKDAY_VERSION,
        applied_facets=APPLIED_FACETS,
        search_text=SEARCH_TEXT)
    return job_postings
