import asyncio
from .job_posting import JobPosting
from json import loads, dumps
from json.decoder import JSONDecodeError
from aiohttp import ClientSession
from .async_request_helpers import fetch_response_text
from bs4 import BeautifulSoup


class SearchFilter:
    """
    A filter in Ultipro job posting search
    
    Attributes:
        fieldName (str): The name of the field to filter on
        values (list(str)): The values to filter by

    Note: the break from naming conventions ("fieldName" not "field_name") is 
    to allow for easier serialization to JSON when making requests.
    """
    
    def __init__(self, fieldName: str, values: list) -> None:
        """
        Constructor
        
        Args:
            fieldName (str): The name of the field to filter on
            values (list(str)): The values to filter by
        """

        if (
            not isinstance(fieldName, str)
            or not isinstance(values, list)
            or not all(isinstance(elem, str) for elem in values)):
            raise Exception("Invalid args.")
        
        self.fieldName = fieldName
        self.values = values
        self.t = "TermsSearchFilterDto"
        self.extra = None


async def get_job_postings(
        Ultipro_or_UKG: str,
        employer_id: str,
        job_board_id: str,
        company: str,
        search_filters: list=[],
        query_string: str="",
        UKG_employer_domain: (str | None)=None
        ) -> list:
    """
    Gets job postings from Ultipro/UKG
    
    Args:
        Ultipro_or_UKG (str): Whether the company uses Ultipro or UKG. Should 
            be one of "Ultipro" or "UKG".
        employer_id (str): The employer's ID in Ultipro/UKG
        job_board_id (str): The job board's ID in Ultipro/UKG
        company (str): The name of the company
        search_filters (list(SearchFilter); default=[]): The filters to search 
            for
        query_string (str, default=""): The query to search for
        UKG_employer_domain (str, None; default=None): If "Ultipro_or_UKG" is 
            "UKG", the employer portion of the UKG domain name.
    Returns:
        list(JobPosting): A list of job postings.
        
    For example, ESL's career search site is 
    "https://recruiting.ultipro.com/ESL1000ESL/JobBoard/0690c0e1-6bba-4977-83bf-9bde86c5080b/JobBoardView/LoadSearchResults"
    where "ultipro.com" indicates the company uses Ultipro and 
    Ultipro_or_UKG should be set to "Ultipro", "ESL100ESL" is the employer_id, 
    "0690c0e1-6bba-4977-83bf-9bde86c5080b" is the job_board_id, and 
    UKG_employer_domain should be set to None as the employer uses Ultipro as 
    opposed to UKG. 
    
    As an additional example, Genessee Regional Bank's career search site is 
    "https://grbbank.rec.pro.ukg.net/GEN1500GNRB/JobBoard/1f082171-3b2f-4eb9-909d-14fc8bcb72b1/JobBoardView/LoadSearchResults"
    where "ukg.net" indicates the company uses UKG and Ultipro_or_UKG should 
    be set to "UKG", "GEN1500GNRB" is the employer_id, 
    "1f082171-3b2f-4eb9-909d-14fc8bcb72b1" is the job_board_is, and "grbbank" 
    is the UKG_employer_domain and should be set as such as the employer uses 
    UKG as opposed to Ultipro.
    
    Check the network tab of your browser when visiting a career site for 
    employer specifics.
    """
    
    if (
        not all(
            isinstance(elem, str) 
            for elem in [
                Ultipro_or_UKG, 
                employer_id, 
                job_board_id, 
                company, 
                query_string])
        or Ultipro_or_UKG not in ["Ultipro", "UKG"]   
        or not (
            isinstance(UKG_employer_domain, str) if Ultipro_or_UKG == "UKG"
            else isinstance(UKG_employer_domain, (str, type(None))))
        or not isinstance(search_filters, list)
        or not all(
            isinstance(search_filter, SearchFilter)
            for search_filter in search_filters)):
        raise Exception("Invalid args.")
    
    base_url =  (
        "https://" + (
            f"{UKG_employer_domain}.rec.pro.ukg.net" if Ultipro_or_UKG == "UKG"
            else "recruiting.ultipro.com")
        + f"/{employer_id}/JobBoard/{job_board_id}/")
    
    search_results_url = base_url + "JobBoardView/LoadSearchResults"
    
    async with ClientSession() as session:
        params = {
            "opportunitySearch": {
                "Top": 50,
                "Skip": 0,
                "QueryString": query_string,
                "Filters": [
                    search_filter.__dict__ for search_filter in search_filters]
            }
        }
        
        job_links = []
        more_to_read = True
        while more_to_read:
            response_text = await fetch_response_text(
                session=session, 
                url=search_results_url, 
                method="POST", 
                params=params)
            response_json = loads(response_text)
            opportunities = response_json["opportunities"]
            job_links += [
                (
                    f"{base_url}OpportunityDetail?opportunityId=" + 
                    opportunity["Id"])
                for opportunity in opportunities]
            params["opportunitySearch"]["Skip"] += 50
            if len(opportunities) == 0:
                more_to_read = False

        async def _get_posting_for_job_link(job_link):
            response_text = await fetch_response_text(
                session=session, url=job_link, method="GET")
            response_soup = BeautifulSoup(response_text, features="lxml")
            page_container = response_soup.find(
                "div", attrs={"id": "PageContainer"})
            script = page_container.find("script")
            posting_info_string = (
                script.text.split("CandidateOpportunityDetail(")[1]
                .split("});")[0] + "}")
            try:
                posting_info = loads(posting_info_string)
            except JSONDecodeError:
                posting_info_string = posting_info_string.encode(
                    "unicode-escape")
                posting_info = loads(posting_info_string)
            
            title = posting_info["Title"]
            
            description_soup = BeautifulSoup(
                posting_info["Description"], features="lxml")
            description = description_soup.get_text("\n").strip()
            
            pay = (
                str(posting_info["CompensationAmount"])
                if "CompensationAmount" in posting_info
                and posting_info["CompensationAmount"]
                else None)
            
            locations = [
                (
                    location["Address"]["City"] 
                    if (
                        isinstance(location.get("Address", None), dict)
                        and isinstance(
                            location["Address"].get("City", None), str))
                    else "Unknown City")
                + ", " + (
                    location["Address"]["State"]["Code"]
                    if (
                        isinstance(location.get("Address", None), dict)
                        and isinstance(
                            location["Address"].get("State", None), dict)
                        and isinstance(
                            location["Address"]["State"].get("Code", None),
                            str))
                    else "Unknown State"
                    )
                for location in posting_info["Locations"]]
            
            job_posting = JobPosting(
                title=title,
                description=description,
                company=company,
                pay=pay,
                link=job_link,
                locations=locations)
            return job_posting
            
        job_postings = await asyncio.gather(
            *[_get_posting_for_job_link(job_link) for job_link in job_links])
        
        return job_postings
