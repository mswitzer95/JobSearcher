from .job_posting import JobPosting
from .async_request_helpers import fetch_response_text
import asyncio
from aiohttp import ClientSession
from json import dumps, loads
from bs4 import BeautifulSoup
from urllib.parse import quote


async def get_job_postings(
        base_domain: str,
        site_number: str,
        location_id: str,
        company: str,
        radius: int=50):
    """
    Gets job postings from Oracle
    
    Args:
        base_domain (str): The base domain of the company's Oracle job site
        site_number (str): The Oracle site number identifier
        location_id (str): The ID of the location within which to search
        company (str): The name of the company hiring for the jobs
        radius (int, default=50): The radius (in miles) within which to search 
            for jobs
    Returns:
        list(JobPosting): A list of job postings

    For example, Cooper Companies' career search site queries 
    "https://hcjy.fa.us2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations,flexFieldsFacet.values,requisitionList.requisitionFlexFields&finder=findReqs;siteNumber=CX_1,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=25,locationId=300000200168003,radius=50,radiusUnit=MI,sortBy=POSTING_DATES_DESC",
    where "https://hcjy.fa.us2.oraclecloud.com/" is the base_domain, "CX_1" is 
    the site_number, and "300000200168003" is the location_id. Check the 
    network tab of your browser when visiting a career site for employer 
    specifics.
    """
    
    if (
        not all(
            isinstance(arg, str) 
            for arg in [base_domain, site_number, location_id, company])
        or not isinstance(radius, int)):
        raise Exception("Invalid args.")
    
    all_requisitions_base_url = (
        base_domain + 
        "hcmRestApi/resources/latest/recruitingCEJobRequisitions")
    all_requisitions_finder_string = ";".join(
        [
            "findReqs",
            ",".join(
                [
                    f"siteNumber={site_number}",
                    (
                        "facetsList=" + 
                        quote(";").join(
                            [
                                "LOCATIONS",
                                "WORK_LOCATIONS",
                                "WORKPLACE_TYPES",
                                "TITLES",
                                "CATEGORIES",
                                "ORGANIZATIONS",
                                "POSTING_DATES",
                                "FLEX_FIELDS"
                            ]
                        )
                    ),
                    "limit=25",
                    f"locationId={location_id}",
                    f"radius={radius}",
                    "radiusUnit=MI",
                    "sortBy=DISTANCE_ASC",
                    "offset={}"
                ]
            )
        ]
    )
    all_requisitions_params = {
        "onlyData": "true",
        "expand": (
            "requisitionList.secondaryLocations,flexFieldsFacet.values," + 
            "requisitionList.requisitionFlexFields"),
    }
    
    async with ClientSession() as session:
        more_to_fetch = True
        offset = 0
        requisition_ids = []
        safe = ",=;%"
        while more_to_fetch:
            all_requisitions_params["finder"] = (
                all_requisitions_finder_string.format(offset))
            response_text = await fetch_response_text(
                session=session,
                url=all_requisitions_base_url,
                method="GET",
                params=all_requisitions_params,
                safe=safe)
            response_json = loads(response_text)
            requisition_list = response_json["items"][0]["requisitionList"]
            requisition_ids += [
                requisition["Id"] for requisition in requisition_list]
            more_to_fetch = (
                response_json["items"][0]["TotalJobsCount"] > 25 + offset)
            if more_to_fetch:
                offset += 25
        
        async def _get_posting_for_requisition_id(requisition_id):
            requisition_base_url = (
                base_domain + 
                "hcmRestApi/resources/latest/" + 
                "recruitingCEJobRequisitionDetails")
            params = {
                "expand": "all",
                "onlyData": "true",
                "finder": (
                    "ById;Id=" + quote(f'"{requisition_id}"') +
                    f",siteNumber={site_number}"
                )
            }
            response_text = await fetch_response_text(
                session=session,
                url=requisition_base_url,
                method="GET",
                params=params,
                safe=safe)
            response_json = loads(response_text)
            
            posting_info = response_json["items"][0]
            
            title = posting_info["Title"]
            
            soup = BeautifulSoup(
                posting_info["ExternalDescriptionStr"], features="lxml")
            description = soup.get_text("\n").strip()
            
            pay = None
            
            link = (
                f"{base_domain}hcmUI/CandidateExperience/en/sites/" + 
                f"{site_number}/job/{requisition_id}/?utm_medium=jobshare")
            
            locations = [posting_info["PrimaryLocation"]]
            locations += [
                location["Name"] 
                for location in posting_info.get("secondaryLocations", [])]

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
                    _get_posting_for_requisition_id(requisition_id)
                    for requisition_id in requisition_ids])
        
    return job_postings
