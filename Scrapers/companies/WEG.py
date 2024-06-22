from ..common_library.Workday_scraper import *

WORKDAY_EMPLOYER_NAME = "wealthenhancement"
CAREER_SITE_NAME = "WEG_Careers"
COMPANY = "Wealth Enhancement Group"
WORKDAY_VERSION = "wd1"
APPLIED_FACETS = {}
SEARCH_TEXT = "NY"


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
