import asyncio
from .job_posting import JobPosting
from json import loads, dumps
from aiohttp import ClientSession
from .async_request_helpers import fetch_response_text
from bs4 import BeautifulSoup
from urllib.parse import unquote

BASE_URL = "https://jobs.dayforcehcm.com/"
BASE_API_URL = f"{BASE_URL}api/jobposting/"
BASE_WEB_PAGE_URL = f"{BASE_URL}en-US/"


async def get_job_postings(
        employer_name: str,
        job_board_name: str,
        company: str,
        location: (str | None)=None,
        distance: (int | None)=15,
        pay_class: (int | None)=None
        ) -> list:
    """
    Gets job postings from Dayforce
    
    Args:
        employer_name (str): The employer's name in Dayforce
        job_board_name (str): The name of the employer's job board in Dayforce
        company (str): The employer's name
        location (str, None; default=None): The location to search for
        distance (int, None; defualt=15): The distance in miles around the 
            location in which to search for postings. Must be non-null if 
            location is not null.
        pay_class (int, None; default=None): The pay class to search for. 
            Typically, 1=full time, 2=part time.
    Returns:
        list(JobPosting): A list of job postings

    For example, Gleason's career search site is
    "https://jobs.dayforcehcm.com/en-US/gleason/CANDIDATEPORTAL"
    where "gleason" is the employer_name and "CANDIDATEPORTAL" is the 
    job_board_name. Through the website, one might submit a parameterized 
    search request of 
    "https://jobs.dayforcehcm.com/en-US/gleason/CANDIDATEPORTAL?locationString=The+Gleason+Works%2C+Rochester%2C+New+York%2C+United+States+of+America&distance=15&payClass=1"
    where "The Gleason Works, Rochester, New York, United Stated of America" 
    is the location, 15 is the distance, and 1 is the pay_class. Check the 
    address bar of your browser when visiting a career site for employer 
    specifics.
    """
    
    if (
        not all(
            isinstance(param, str) 
            for param in [employer_name, job_board_name, company])
        or not isinstance(pay_class, (int, type(None)))
        or not (
            (
                isinstance(location, str) 
                and isinstance(distance, int))
            or (
                isinstance(location, type(None)))
                and isinstance(distance, (int, type(None))))):
        raise Exception("Invalid args.")

    async with ClientSession() as session:
        base_job_board_url = (
            f"{BASE_WEB_PAGE_URL}{employer_name}/{job_board_name}/")
        # Making initial request to job board to set session cookies and get 
        # X-CSRF token 
        async with session.get(base_job_board_url) as response:
            cookies = [
                header[1].split(";")[0].split("=") 
                for header in response.headers.items()
                if header[0] == "Set-Cookie"]
            cookies = {
                cookie[0]: cookie[1]
                for cookie in cookies}
        session.cookie_jar.update_cookies(cookies)
        tokens = (
            unquote(cookies.get("__Host-next-auth.csrf-token"))
            .split("|"))
        headers = {"X-Csrf-Token": tokens[0]}

        search_api_url = f"{BASE_API_URL}search"
        params = {
            "clientNamespace": employer_name,
            "cultureCode": "en-US",
            "jobBoardCode": job_board_name,
            "paginationStart": 0,
        }
        if distance:
            params["distance"] = distance
            params["distanceUnit"] = 0
        if location:
            params["locationString"] = location
        if pay_class:
            params["payClass"] = pay_class

        job_ids_and_job_board_ids = []
        more_to_read = True
        while more_to_read:
            response_text = await fetch_response_text(
                    session=session, 
                    url=search_api_url, 
                    method="POST", 
                    params=params,
                    headers=headers)
            response_json = loads(response_text)
            postings = response_json["jobPostings"]
            job_ids_and_job_board_ids += [
                (posting["jobPostingId"], posting["jobBoardId"]) 
                for posting in postings]
            params["paginationStart"] += 25
            if len(postings) == 0:
                more_to_read = False

        async def _get_posting_for_job_id(job_id, job_board_id):
            api_link = (
                f"{BASE_API_URL}{employer_name}/en-US/{job_board_id}/{job_id}")
            response_text = await fetch_response_text(
                session=session,
                url=api_link,
                method="GET",
                headers=headers)
            posting_info = loads(response_text)
            
            title = posting_info["jobTitle"]

            description_contents = list(
                posting_info["jobPostingContent"].values())
            description = (
                "\n".join(
                    [
                        (
                            BeautifulSoup(content, features="lxml")
                        ).get_text("\n").strip()
                        for content in description_contents
                        if content and len(content) > 0]))
            
            attributes = {
                attribute["name"]: attribute["value"] 
                for attribute in posting_info["jobPostingAttributes"]}
            if (
                "HiringMinRate" not in attributes 
                and "HiringMaxRate" not in attributes):
                pay = "Unknown"
            else:
                pay = (
                    str(attributes.get("HiringMinRate", "Unknown")) + " - " +
                    str(attributes.get("HiringMaxRate", "Unknown")))
            
            link = f"{base_job_board_url}jobs/{job_id}"
            
            locations_json = posting_info["postingLocations"]
            locations = [
                (
                    location["cityName"] 
                    if location["cityName"] else "Unknown City") 
                + ", " + (
                    location["stateCode"]
                    if location["stateCode"] else "Unknown State")
                for location in locations_json]
            
            job_posting = JobPosting(
                title=title,
                description=description,
                company=company,
                pay=pay,
                link=link,
                locations=locations)
            return job_posting
    
        job_postings = await asyncio.gather(
                *[
                    _get_posting_for_job_id(job_id, job_board_id) 
                    for (job_id, job_board_id) in job_ids_and_job_board_ids])
        
    return job_postings