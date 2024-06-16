from job_posting import JobPosting
from datetime import datetime
from json import loads
from bs4 import BeautifulSoup
import asyncio
from aiohttp import ClientSession
from async_request_helpers import fetch_response_text
from urllib.parse import urlencode

BASE_URL = "https://workforcenow.adp.com/mascsr/default/"
REQUISITIONS_URL_SUFFIX = "careercenter/public/events/staffing/v1/job-requisitions"
POSTING_URL_SUFFIX = "mdf/recruitment/recruitment.html"


async def get_job_postings(
        c_id: str,
        company: str,
        top: int=1000,
        cc_id: str="19000101_000001") -> list:
    """
    Gets job postings from ADP
    
    Args:
        c_id (str): The c ID of the specific employer
        company (str): The company that posted the job
        top (int, default=1000): The number of job openings to retrieve
        ccId (str, default="19000101_000001"): The cc ID (unsure what this is, 
            seems to always be "19000101_000001")
    Returns:
        list(JobPosting): A list of job postings
    """
    
    if (
        not all(isinstance(arg, str) for arg in [c_id, cc_id])
        or not isinstance(top, int)):
        raise Exception("Got invalid args.")
    async with ClientSession() as session:
        requisition_params = {
            "cid": c_id,
            "timeStamp": int(datetime.now().timestamp()),
            "lang": "en_US",
            "ccId": cc_id,
            "locale": "en_US",
            "$top": top
        }
        url = BASE_URL + REQUISITIONS_URL_SUFFIX
        response_text = await fetch_response_text(
            session=session, url=url, method="GET", params=requisition_params)
        response_json = loads(response_text)
        jobs = response_json["jobRequisitions"]
        job_ids = [
            job["customFieldGroup"]["stringFields"][0]["stringValue"]
            for job in jobs
        ]
    
        requisition_params.pop("$top")
        async def _get_posting_for_job_id(job_id):
            url = BASE_URL + REQUISITIONS_URL_SUFFIX + "/" + job_id
            response_text = await fetch_response_text(
                session=session,
                url=url,
                method="GET",
                params=requisition_params)
            response_json = loads(response_text)
        
            title = response_json["requisitionTitle"]

            soup = BeautifulSoup(
                response_json["requisitionDescription"], features="lxml")
            description = soup.get_text("\n").strip()

            if "payGradeRange" in response_json:
                pay_grade_range = response_json["payGradeRange"]
                minimum_rate = pay_grade_range["minimumRate"]["amountValue"]
                maximum_rate = pay_grade_range["maximumRate"]["amountValue"]
                pay = f"{minimum_rate} - {maximum_rate}"
            else:
                pay = "N/A"
        
            locations = [
                location["nameCode"]["shortName"].strip()
                for location in response_json["requisitionLocations"]]

            posting_params = {
                "cid": c_id,
                "ccId": cc_id,
                "jobId": job_id,
                "lang": "en_US"
            }
            posting_query_string = urlencode(posting_params)
            link = BASE_URL + POSTING_URL_SUFFIX + "?" + posting_query_string
            
            job_posting = JobPosting(
                title=title, 
                description=description, 
                company=company, 
                pay=pay, 
                link=link, 
                locations=locations)
            return job_posting
        
        job_postings = await asyncio.gather(
            *[_get_posting_for_job_id(job_id) for job_id in job_ids])

    return job_postings
