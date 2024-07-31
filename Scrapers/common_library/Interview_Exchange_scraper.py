import asyncio
from .job_posting import JobPosting
from json import loads, dumps
from aiohttp import ClientSession
from .async_request_helpers import fetch_response_text
from bs4 import BeautifulSoup


async def get_job_postings(
        domain_prefix: str,    
        company_id: str,
        company: str) -> list:
    """
    Gets job postings from Interview Exchange
    
    Args:
        domain_prefix (str): The company's Interview Exchange domain prefix
        company_id (str): The ID of the company in Interview Exchange
        company (str): The name of the company
    Returns:
        list(JobPosting): The job postings

    When attempting to determine the correct variables to pass, one should 
    look for the company's Interview Exchange RSS feed. For exmaple, Alfred 
    State's Interview Exchange RSS feed is:
    "https://alfredstate.interviewexchange.com/jobsrss.jsp?COMPANYID=481"
    where "alfredstate" is the domain_prefix and "481" is the company_id.
    """
    
    if not all(
        isinstance(arg, str) for arg in [domain_prefix, company_id, company]):
        raise Exception("Invalid args.")

    postings_url = (
        f"https://{domain_prefix}.interviewexchange.com/jobsrss.jsp?" + 
        f"COMPANYID={company_id}")
    async with ClientSession() as session:
        response_text = await fetch_response_text(
                session=session, 
                url=postings_url, 
                method="GET")
        soup = BeautifulSoup(response_text, features="xml")
        xml_job_postings = soup.find_all("item")
        job_postings = [
            JobPosting(
                title=xml_job_posting.find("title").get_text("\n").strip(),
                description=(
                    BeautifulSoup(
                        xml_job_posting.find("description").get_text("\n"),
                        features="lxml"
                    ).get_text("\n").strip()),
                company=company, 
                pay=None,
                link=xml_job_posting.find("link").get_text("\n").strip(),
                locations=[
                    xml_job_posting.find("location").get_text("\n").strip()])
            for xml_job_posting in xml_job_postings
        ]
        
    return job_postings
