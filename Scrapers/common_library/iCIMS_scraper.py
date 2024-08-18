import asyncio
from .job_posting import JobPosting
from json import loads, dumps
from aiohttp import ClientSession
from .async_request_helpers import fetch_response_text
from bs4 import BeautifulSoup
from urllib.parse import unquote


async def get_job_postings(
        domain_name: str,
        company: str,
        locations: list=[]) -> list:
    """
    Gets job postings from iCIMS
    
    Args:
        domain_name (str): The domain of the company's job search site on iCIMS
        company (str): The company to get jobs for
        locations (list(str), default=[]): The locations to search for jobs
    Returns:
        list(JobPosting): The job postings

    For example, Heritage Christian Service's iCIMS job search site while 
    searching the "US-NY-Amherst and surrounding areas" location is
    "https://careers-heritagechristianservices.icims.com/jobs/search?ss=1&searchLocation=12781-12816-Amherst+and+surrounding+areas"
    where "https://careers-heritagechristianservices.icims.com/" is the 
    domain_name and "12781-12816-Amherst+and+surrounding+areas" is a location 
    in locations.
    """
    
    if (
        not all(isinstance(arg, str) for arg in [domain_name, company])
        or not isinstance(locations, list)
        or not all(isinstance(location, str) for location in locations)):
        raise Exception("Invalid args.")
    
    all_jobs_url = f"{domain_name}jobs/search"
    
    async with ClientSession() as session:
        async def _get_job_links_for_location(location):
            params = {
                "ss": 1,
                "pr": 0,
                "in_iframe": 1,
                "searchLocation": unquote(location)
            }
            job_links = []
            more_to_fetch = True
            while more_to_fetch:
                response_text = await fetch_response_text(
                    session=session,
                    url=all_jobs_url,
                    method="GET",
                    params=params,
                    safe="+")
                soup = BeautifulSoup(response_text, features="lxml")
                job_link_tags = soup.find_all(
                    lambda tag: 
                        "iCIMS_Anchor" in tag.get("class", [])
                        and tag.has_attr("title"))
                new_job_links = [
                    job_link_tag.get("href")
                    for job_link_tag in job_link_tags]
                job_links += new_job_links
                more_to_fetch = len(new_job_links) > 0
                if more_to_fetch:
                    params["pr"] += 1
            return job_links

        if len(locations) == 0:
            locations = [""]
        job_links = await asyncio.gather(
            *[_get_job_links_for_location(location) for location in locations])
        job_links = list(set(sum(job_links, [])))

        async def _get_posting_for_job_link(job_link):
            response_text = await fetch_response_text(
                session,
                url=job_link,
                method="GET")
            soup = BeautifulSoup(response_text, features="lxml")
            job_content = soup.find(
                None, attrs={"class": "iCIMS_JobContent"})

            title_element = job_content.find(
                None, attrs={"class": "iCIMS_Header"})
            title = title_element.get_text().strip()

            description_elements = job_content.find_all(
                lambda tag: "iCIMS_InfoMsg" in tag.get("class",[""])[0])
            description = "\n".join(
                tag.get_text("\n").strip() for tag in description_elements)
            
            locations_elements_parent = (
                job_content.find(
                    lambda tag:
                        " ".join(
                            tag.get("class", [""])) == "sr-only field-label"
                        and tag.get_text() == "Job Locations"
                ).parent
            )
            locations_elements = locations_elements_parent.find_all(
                lambda tag: 
                    " ".join(
                            tag.get("class", [""])) != "sr-only field-label")
            locations_text = " ".join(
                [
                    location.get_text(" ").strip() 
                    for location in locations_elements])
            locations = [
                location.strip() for location in locations_text.split("|")]

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
                    _get_posting_for_job_link(job_link)
                    for job_link in job_links])
        return job_postings