import asyncio
from urllib import response
from .job_posting import JobPosting
from json import loads, dumps
from aiohttp import ClientSession
from .async_request_helpers import fetch_response_text
from bs4 import BeautifulSoup


async def get_job_postings(
        domain_name: str,
        company: str,
        location: str="",
        ) -> list:
    """
    Gets job postings from SAP SuccessFactors
    
    Args:
        domain_name (str): The domain name of the company's job search site
        company (str): The company to get job postings for
        location (str, default=""): The location to search for
    Returns:
        list(JobPosting): The job postings

    For example, Seneca Food's job search site is 
    "https://careers.senecafoods.com/", where
    "https://careers.senecafoods.com/" is the domain_name.
    
    Note that SuccessFactors is a white labeled product and is often difficult 
    to identify. Some example of company job posting sites that use 
    SuccessFators are "https://careers.carestream.com/search/", 
    "https://careers.kodak.com/search/", and 
    "https://careers.senecafoods.com/search/".
    """
    
    if not all(
        isinstance(arg, str) for arg in [domain_name, company, location]):
        raise Exception ("Invalid args.")
    
    all_jobs_url = f"{domain_name}search/"
    params = {
        "location": location,
        "startrow": 0
    }
    
    async with ClientSession() as session:
        more_to_fetch = True
        job_links_and_titles = []
        while more_to_fetch:
            response_text = await fetch_response_text(
                    session=session, 
                    url=all_jobs_url, 
                    method="GET",
                    params=params)
            soup = BeautifulSoup(response_text, features="lxml")
            if soup.find(None, attrs={"id": "noresults"}):
                more_to_fetch = False
                continue
            job_link_tags = soup.find_all("a", attrs={"class": "jobTitle-link"})
            
            new_job_links_and_titles = [
                (f"{domain_name}{tag.get('href')}", tag.get_text("\n").strip()) 
                for tag in job_link_tags]
            new_job_links_and_titles = list(set(new_job_links_and_titles))
            job_links_and_titles += new_job_links_and_titles
            params["startrow"] += 25

        async def _get_posting_for_link_and_title(job_link, title):
            response_text = await fetch_response_text(
                session=session,
                url=job_link,
                method="GET")
            soup = BeautifulSoup(response_text, features="lxml")
            
            description_element = soup.find(
                "div", attrs={"class": "jobDisplay"})
            description = description_element.get_text("\n").strip()
            
            locations = [
                tag.get_text("\n").strip() for tag
                in soup.find_all("span", attrs={"class": "jobGeoLocation"})]
            
            job_posting = JobPosting(
                title=title,
                description=description,
                company=company, 
                pay=None,
                link=job_link,
                locations=locations)
            return job_posting

        job_postings = await asyncio.gather(
                *[
                    _get_posting_for_link_and_title(job_link, title)
                    for (job_link, title) in job_links_and_titles])
    return job_postings