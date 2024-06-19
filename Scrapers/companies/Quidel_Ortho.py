from common_library.Workday_scraper import *

WORKDAY_EMPLOYER_NAME = "orthoclinical"
CAREER_SITE_NAME = "search"
COMPANY = "Quidel Ortho"
WORKDAY_VERSION = "wd1"
APPLIED_FACETS = {
    # NY region
    "Location_Region_State_Province": [
        "9819bf0148e54f89adb255aa7bead635"
    ],
    # Finance job family
    "jobFamilyGroup": [
        "386ae06b729c1000cdaa693ef3320000"
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
