from pydoc import describe
from job_posting import JobPosting
from async_request_helpers import fetch_response_text
import asyncio
from aiohttp import ClientSession
from json import dumps, loads
from bs4 import BeautifulSoup


async def get_job_postings(
        Workday_employer_name: str,
        career_site_name: str,
        company: str,
        applied_facets: dict={},
        search_text: str="") -> list:
    """
    Gets job postings
    
    Args:
        Workday_employer_name (str): The employer's name in Workday
        career_site_name (str): The employer's career site name in Workday
        company (str): The employer hiring for the jobs
        applied_facets (dict, default={}): The search criteria
        searc_text (str, default=""): The text to search for
    Returns:
        list(JobPosting): A list of job postings
    """
    
    if (
        not all(
            isinstance(arg, str)
            for arg in [
                Workday_employer_name, career_site_name, company, search_text])
        or not isinstance(applied_facets, dict)):
        raise Exception("Invalid args.")
    
    base_url = (
        f"https://{Workday_employer_name}.wd5.myworkdayjobs.com/wday/cxs/" + 
        f"{Workday_employer_name}/{career_site_name}")
    url = base_url + "/jobs"
    limit = 20
    offset = 0
    params = {
        "appliedFacets": applied_facets,
        "limit": limit,
        "offset": offset,
        "searchText": search_text
    }
    headers = {"Content-Type": "application/json"}
    async with ClientSession(headers=headers) as session:
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
            offset += 20
            if offset > total:
                more_to_read = False

        async def _get_posting_for_job_link(job_link):
            response_text = await fetch_response_text(
                session=session, url=job_link, method="GET")
            response_json = loads(response_text)
            posting_info = response_json["jobPostingInfo"]
            
            title = posting_info["title"]
            
            soup = BeautifulSoup(
                posting_info["jobDescription"], features="lxml")
            description = soup.get_text("\n").strip()
            
            pay = "N/A"
            
            link = posting_info["externalUrl"]
            
            locations = [posting_info["location"]]
            if "additionalLocations" in posting_info:
                locations += posting_info["additionalLocations"]

            job_posting = JobPosting(
                title=title,
                description=description,
                company=company, pay=pay,
                link=link,
                locations=locations)
            return job_posting
        
        job_postings = await asyncio.gather(
            *[_get_posting_for_job_link(job_link) for job_link in job_links])
        
        return job_postings