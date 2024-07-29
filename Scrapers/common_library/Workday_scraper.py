from .job_posting import JobPosting
from .async_request_helpers import fetch_response_text
import asyncio
from aiohttp import ClientSession
from json import dumps, loads
from bs4 import BeautifulSoup


async def get_job_postings(
        Workday_employer_name: str,
        career_site_name: str,
        company: str,
        Workday_version: str,
        applied_facets: dict={},
        search_text: str="") -> list:
    """
    Gets job postings from Workday
    
    Args:
        Workday_employer_name (str): The employer's name in Workday
        career_site_name (str): The employer's career site name in Workday
        company (str): The employer hiring for the jobs
        Workday_version (str): The Workday version for requesting jobs; is 
            typically "wd5" or "wd1"
        applied_facets (dict, default={}): The search criteria, specific to 
            the employer
        searc_text (str, default=""): The text to search for
    Returns:
        list(JobPosting): A list of job postings

    For example, Keybank's career search site queries 
    "https://keybank.wd5.myworkdayjobs.com/wday/cxs/keybank/External_Career_Site/jobs",
    where "keybank" is the Workday_employer_name, "External_Career_Site" is 
    the career_site_name, and "wd5" is the workday_version. The applied facets 
    and search text are included in the request payload made by the career 
    search site. Check the network tab of your browser when visiting a career 
    site for employer specifics.
    """
    
    if (
        not all(
            isinstance(arg, str)
            for arg in [
                Workday_employer_name, 
                career_site_name, 
                company, 
                search_text,
                Workday_version])
        or not isinstance(applied_facets, dict)):
        raise Exception("Invalid args.")
    
    base_url = (
        f"https://{Workday_employer_name.lower()}.{Workday_version.lower()}" + 
        f".myworkdayjobs.com/wday/cxs/{Workday_employer_name.lower()}" + 
        f"/{career_site_name.lower()}")
    url = base_url + "/jobs"
    params = {
        "appliedFacets": applied_facets,
        "limit": 20,
        "offset": 0,
        "searchText": search_text
    }
    async with ClientSession() as session:
        response_text = await fetch_response_text(
            session=session, url=url, method="POST", params=params)
        response_json = loads(response_text)
        total = response_json["total"]
        job_links = []
        more_to_read = True
        while more_to_read:
            job_links += [
                base_url + posting["externalPath"]
                for posting in response_json["jobPostings"]
            ]
            params["offset"] += 20
            if params["offset"] > total:
                more_to_read = False
            if more_to_read:
                response_text = await fetch_response_text(
                    session=session, url=url, method="POST", params=params)
                response_json = loads(response_text)

        async def _get_posting_for_job_link(job_link):
            response_text = await fetch_response_text(
                session=session, url=job_link, method="GET")
            response_json = loads(response_text)
            posting_info = response_json["jobPostingInfo"]
            
            title = posting_info["title"]
            
            soup = BeautifulSoup(
                posting_info["jobDescription"], features="lxml")
            description = soup.get_text("\n").strip()
            
            pay = None
            
            link = posting_info["externalUrl"]
            
            locations = [posting_info["location"]]
            if "additionalLocations" in posting_info:
                locations += posting_info["additionalLocations"]

            job_posting = JobPosting(
                title=title,
                description=description,
                company=company,
                pay=pay,
                link=link,
                locations=locations)
            return job_posting
        
        job_postings = await asyncio.gather(
            *[_get_posting_for_job_link(job_link) for job_link in job_links])
        
        return job_postings