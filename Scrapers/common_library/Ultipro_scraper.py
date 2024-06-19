import asyncio


class SearchFilter:
    """
    A filter in Ultipro job posting search
    
    Attributes:
        fieldName (str): The name of the field to filter on
        values (list(str)): The values to filter by
    """
    
    def __init__(self, fieldName: str, values: list):

async def get_job_postings(
        base_url: str,
        Ultipro_employer_name: str,
        Utlipro_employer_id: str,
        ) -> list:
    """
    Gets job postings from Ultipro/UKG Pro
    
    Args:
        base_url (str): The base url to request
        
    """
    
    # TO DO

    