import asyncio
from .job_posting import JobPosting
from json import loads, dumps
from aiohttp import ClientSession
from .async_request_helpers import fetch_response_text


async def get_job_postings(
        domain_name: str,
        company: str,
        location: str="",
        radius: int=50) -> list:
    """
    Gets job postings from Jibe
    
    Args:
        domain_name (str): The domain name of the company job site
        company (str): The company to get jobs for
        location (str; default=""): The location around which to search for 
            jobs
        radius (int; default=50): The radius (in miles) around the location 
            within which to search
    Returns:
        list(JobPosting): The job postings

    For example, Paychex's job posting site is 
    "https://careers.paychex.com/careers/jobs", where 
    "https://careers.paychex.com/" is the domain_name. The location arg should 
    be optionally set by finding the desired location in the location search 
    bar on the relevant job posting site.
    
    Note that Jibe is a white labeled product and is often difficult to 
    identify. Some example of company job posting sites that use Jibe are 
    "https://careers.paychex.com/careers/jobs" and 
    "https://careers.tompkinsfinancial.com/jobs".
    """
    
    if (
        not all(
            isinstance(arg, str)
            for arg in [domain_name, company, location])
        or not isinstance(radius, int)):
        raise Exception("Invalid args.")

    async with ClientSession() as session:
        all_jobs_url = f"{domain_name}api/jobs"
        all_jobs_params = {
            "page": 1,
            "location": location,
            "stretchUnit": "MILES",
            "stretch": radius,
            "limit": 100
        }
        more_to_fetch = True
        job_postings = []
        while more_to_fetch:
            response_text = await fetch_response_text(
                session=session, 
                url=all_jobs_url, 
                method="GET",
                params=all_jobs_params)
            response_json = loads(response_text)
            jobs = response_json["jobs"]
            
            for job in [job["data"] for job in jobs]:
                title = job["title"]
                description = job["description"]
                link = f"{domain_name}careers/jobs/{job['req_id']}"
                locations = job["full_location"].split("; ")
                job_posting = JobPosting(
                    title=title,
                    description=description,
                    company=company,
                    pay=None,
                    link=link,
                    locations=locations)
                job_postings.append(job_posting)

            more_to_fetch = len(jobs) > 0
            if more_to_fetch:
                all_jobs_params["page"] += 1

    return job_postings
