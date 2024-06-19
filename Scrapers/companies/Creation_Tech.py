from common_library.Workday_scraper import *

WORKDAY_EMPLOYER_NAME = "creationtech"
CAREER_SITE_NAME = "creation"
COMPANY = "Creation Tech"
WORKDAY_VERSION = "wd1"
APPLIED_FACETS = {
    # Newark NY location
    "locations": [
        "56c156f6ce6d0100fd0d04de62370000"
    ],
    # Finance job family
    "jobFamilyGroup": [
        "a0084ac26eec0178e6a0d1b1200c1b8e"
    ]
}
SEARCH_TEXT = ""


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
