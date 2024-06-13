
class JobPosting:
    """
    A job posting
    
    Attributes:
        title (str): The title of the job the posting is for
        description (str): The description of the job the posting is for
        company (str): The company that posted the job
    """
    
    def __init__(self, title: str, description: str, company: str) -> None:
        """
        Constructor
        
        Args:
            title (str): The title of the job the posting is for
            description (str): The description of the job the posting is for
            company (str): The company that posted the job
        """
        
        if not all(
            isinstance(arg, str) for arg in [title, description, company]):
            raise Exception("Invalid inputs when trying to instantiate " + 
                            "JobPosting.")
        
        self.title = title
        self.description = description
        self.company = company
