from ..common_library.Dayforce_scraper import *

# NOTE TWO CAREER SITES

EMPLOYER_NAME = "epilepsypralid"
JOB_BOARD_NAME_1 = "CANDIDATEPORTAL"
JOB_BOARD_NAME_2 = "SDCANDIDATEPORTAL"
COMPANY = "Empowering People's Independence"
LOCATION = None
PAY_CLASS = None #1

async def main():
    """
    Scrapes postings and returns them.
    Args: None
    Returns:
        list(JobPosting): The job postings scraped
    """
    job_postings = await asyncio.gather(
        *[
            get_job_postings(
                employer_name=EMPLOYER_NAME,
                job_board_name=job_board_name,
                company=COMPANY,
                location=LOCATION,
                pay_class=PAY_CLASS)
            for job_board_name in [JOB_BOARD_NAME_1, JOB_BOARD_NAME_2]])
    job_postings = sum(job_postings, [])
    return job_postings
