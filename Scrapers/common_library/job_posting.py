
class JobPosting:
    """
    A job posting
    
    Attributes:
        title (str): The title of the job the posting is for
        description (str): The description of the job the posting is for
        company (str): The company that posted the job
        pay (str, None): The pay rate of the job
        link (str): The link to the job posting
        location (list(str)): The locations of the job
    """
    
    def __init__(
            self,
            title: str,
            description: str,
            company: str,
            pay: str | None,
            link: str,
            locations: list) -> None:
        """
        Constructor
        
        Args:
            title (str): The title of the job the posting is for
            description (str): The description of the job the posting is for
            company (str): The company that posted the job
            pay (str): The pay rate of the job
            link (str): The link to the job posting
            locations (list(str)): The locations for the job
        """
        
        if (
            not all(
                isinstance(arg, str) 
                for arg in [title, description, company, link])
            or not isinstance(pay, (str, type(None)))    
            or not isinstance(locations, list)
            or not all(isinstance(location, str) for location in locations)):
            raise Exception("Invalid inputs.")
        
        self.title = title
        self.description = description
        self.company = company
        self.pay = pay
        self.link = link
        self.locations = locations
