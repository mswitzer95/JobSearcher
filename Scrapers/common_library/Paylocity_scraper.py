import asyncio
from .job_posting import JobPosting
from json import loads, dumps
from aiohttp import ClientSession
from .async_request_helpers import fetch_response_text
from bs4 import BeautifulSoup

BASE_SEARCH_URL = "https://recruiting.paylocity.com/recruiting/jobs/All/"
BASE_DETAILS_URL = "https://recruiting.paylocity.com/Recruiting/Jobs/Details/"


async def get_job_postings(
        employer_id: str,
        employer_name: str,
        company: str,
        search: (str | None)=None,
        location: (str | None)=None,
        department: (str | None)=None) -> list:
    """
    Gets job postings from Paylocity
    
    Args:
        employer_id (str): The employer's ID in Paylocity
        employer_name (str): The employer's name in Paylocity
        company (str): The name of the company
        search (str, None; default=None): The query to search for
        location (str, None; default=None): The location to search for
        departmnet (str, None; default=None): The department to search for
    Returns:
        list(JobPosting): A list of job postings.

    For example, Keuka College's career search site is 
    https://recruiting.paylocity.com/recruiting/jobs/All/79f94d92-d2c7-407b-923b-2c8ba8a4a263/Keuka-College-Faculty-Staff"
    where "79f94d92-d2c7-407b-923b-2c8ba8a4a263" is the employer_id, and
    "Keuka-College-Faculty Staff" is the employer_name. Through the website, 
    one might submit a parameterized request of:
    "https://recruiting.paylocity.com/recruiting/jobs/All/79f94d92-d2c7-407b-923b-2c8ba8a4a263/Keuka-College-Faculty-Staff?search=professor&location=Keuka%20College%20Main%20Campus&department=Academic%20Affairs"
    where "professor" is the search, "Keuka College Main Campus" is the 
    location, and "Academic Affairs" is the department. Check the address bar 
    of your browser when visiting a career site for employer specifics.
    """
    
    if (
        not all(
            isinstance(param, str) 
            for param in [employer_id, employer_name, company])
        or not all(
            isinstance(param, (str, type(None)))
            for param in [search, location, department])):
        raise Exception("Invalid args.")
    
    params = {}
    for param_name, param in [
        ("search", search),
        ("location", location),
        ("department", department)]:
        if param:
            params[param_name] = param
    search_results_url = f"{BASE_SEARCH_URL}{employer_id}/{employer_name}"
    async with ClientSession() as session:
        response_text = await fetch_response_text(
                session=session, 
                url=search_results_url, 
                method="GET", 
                params=params)
        response_soup = BeautifulSoup(response_text, features="lxml")
        script = response_soup.find(
            lambda tag: tag.name == "script" and "pageData" in tag.text)
        script_text = script.text
        jobs = loads(
            script_text[
                script_text.index("{"):
                script_text.rindex("}") + 1])["Jobs"]
        jobs = [
            job for job in jobs if job["ShouldDisplayLocation"]]
        if location:
            jobs = [
                job for job in jobs if job["LocationName"] == location]
        if department:
            jobs = [
                job for job in jobs if job["HiringDepartment"] == department]  
        job_ids = [job["JobId"] for job in jobs]
        
        async def _get_posting_for_job_id(job_id):
            details_url = f"{BASE_DETAILS_URL}/{job_id}"
            response_text = await fetch_response_text(
                session=session, 
                url=details_url, 
                method="GET")
            response_soup = BeautifulSoup(response_text, features="lxml")
            script = response_soup.find(
                lambda tag: 
                    tag.name == "script" 
                    and '"@type":"JobPosting"' in tag.text)
            script_text = script.text
            posting_info = loads(
                script_text[
                    script_text.index("{"):
                    script_text.rindex("}") + 1])
            
            title = posting_info["title"]
            
            description_soup = BeautifulSoup(
                posting_info["description"], features="lxml")
            description = description_soup.get_text("\n").strip()
            
            if "baseSalary" in posting_info:
                base_salary = posting_info["baseSalary"]    
                if "value" in base_salary["value"]:
                    pay = str(base_salary["value"]["value"])
                else:
                    pay = (
                        str(posting_info["baseSalary"]["value"]["minValue"])
                        + "-"
                        + str(posting_info["baseSalary"]["value"]["minValue"]))
            else:
                pay = None    

            
            locality = (
                posting_info["jobLocation"]["address"]["addressLocality"])
            region = (
                posting_info["jobLocation"]["address"]["addressRegion"])
            locations = [locality + ", " + region]
            
            job_posting = JobPosting(
                title=title,
                description=description,
                company=company, pay=pay,
                link=details_url,
                locations=locations)
            return job_posting
        
        job_postings = await asyncio.gather(
            *[_get_posting_for_job_id(job_id) for job_id in job_ids])
        
        return job_postings
