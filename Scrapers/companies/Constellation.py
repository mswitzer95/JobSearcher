from ..common_library.Workday_scraper import *

WORKDAY_EMPLOYER_NAME = "cbrands"
CAREER_SITE_NAME = "CBI_External_Careers"
COMPANY = "Constellation Brands"
WORKDAY_VERSION = "wd5"
APPLIED_FACETS = {
    # Finance and accounting job family
    #"jobFamilyGroup": [
    #    "c9530756020a10c56f194aabc62f05ea"
    #]
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
