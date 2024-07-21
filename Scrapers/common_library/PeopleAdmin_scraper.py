import asyncio
from .job_posting import JobPosting
from json import loads, dumps
from aiohttp import ClientSession
from .async_request_helpers import fetch_response_text
from bs4 import BeautifulSoup


async def get_job_postings(
        domain_name: str,
        company: str) -> list:
    """
    Gets job postings from PeopleAdmin/PowerSchool
    
    Args:
        domain_name (str): The domain name of the job posting site
        company (str): The name of the company
    Returns:
        list(JobPosting): The job postings
    
    For example, Saint John Fisher's job posting site is 
    "https://jobs.sjf.edu/", where "https://jobs.sjf.edu" is the domain_name.
    
    Note that PeopleAdmin is a white labeled product and is often difficult 
    to identify. Some example of company job posting sites that use 
    PeopleAdmin are "https://jobs.sjf.edu/", "https://jobs.naz.edu/", and 
    "https://jobs.geneseo.edu/".
    """
    
    if not all(isinstance(arg, str) for arg in [domain_name, company]):
        raise Exception ("Invalid args.")
    
    postings_url = f"{domain_name}/postings/all_jobs.atom"
    
    async with ClientSession() as session:
        response_text = await fetch_response_text(
                session=session, 
                url=postings_url, 
                method="GET")
        soup = BeautifulSoup(response_text, features="xml")
        job_titles_and_links = [
            (
                entry.find("title").text,
                entry.find("link").attrs["href"])
            for entry in soup.find_all("entry")]
        
        async def _get_posting_for_job_link(job_link, job_title):
            response_text = await fetch_response_text(
                session=session,
                url=job_link,
                method="GET")
            soup = BeautifulSoup(response_text, features="lxml")
            form_tab = soup.find("div", id="form_view")
            description = form_tab.get_text("\n").strip()
            pay="Unknown"
            locations=[]
            job_posting = JobPosting(
                title=job_title,
                description=description,
                company=company, 
                pay=pay,
                link=job_link,
                locations=locations)
            return job_posting
        
        job_postings = await asyncio.gather(
            *[
                _get_posting_for_job_link(job_link, job_title)
                for (job_title, job_link) in job_titles_and_links])
        
        return job_postings