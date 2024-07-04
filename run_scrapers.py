from os import path, listdir
from json import dumps
from tqdm.asyncio import tqdm
import asyncio
from importlib import import_module
import logging
from random import shuffle

COMPANIES_DIR = path.join(".", "scrapers", "companies")
RESULTS_FILE_NAME = path.join(".", "web_app", "public", "scraper_results.json")
SCRAPER_FILES = [
    file_name for file_name in listdir(COMPANIES_DIR)
    if path.splitext(file_name)[-1] == ".py"
    and path.splitext(file_name)[0] != "__init__"
]
SCRAPER_MODULES = [
    import_module("." + module, package="scrapers.companies") for module in [
        path.splitext(file_name)[0] for file_name in SCRAPER_FILES
    ]
]

# Setting up logging
LOGGING_FILE_NAME = path.join(".", "scrapers", "scraper_results.log")
open(LOGGING_FILE_NAME, mode="w").close()
logging.basicConfig(filename=LOGGING_FILE_NAME, level=logging.DEBUG)
LOGGER = logging.getLogger()


async def main():
    """
    Runs all scrapers in the "companies" directory
    """
    
    semaphore = asyncio.Semaphore(3)
    
    # Wrapper with error handling, semaphore usage, and logging for main 
    # function in each scraper module
    async def _try_scraper(module):
        async with semaphore:
            try:
                postings = await module.main()
                LOGGER.info(f"Found {len(postings)} job postings for " + 
                            f"{module.COMPANY}.")
            except Exception as exception:
                LOGGER.warning(f"Got exception for {module.COMPANY}.")
                LOGGER.exception(exception)
                postings = []
            return postings
    
    scraper_tries = [_try_scraper(module) for module in SCRAPER_MODULES]
    shuffle(scraper_tries)
    all_postings = await tqdm.gather(*scraper_tries)
    all_postings = sum(all_postings, [])
    with open(RESULTS_FILE_NAME, mode="w") as file:
        file.write(dumps(all_postings, default=lambda i: i.__dict__))
        LOGGER.info(f"Job postings written to {RESULTS_FILE_NAME}.")

    print(f"Logs written to {LOGGING_FILE_NAME}.")


if __name__ == "__main__":
    asyncio.run(main())
