# JobSearcher
This project scrapes job postings from multiple company career websites and displays them all on a singular page in a web-app.


## TO DO
The following are potential future areas of improvement to the project.
* Additional scrapers for more companies
* Two "views" on the web app: one showing all postings at once in a scrollable list; and another showing only one posting at once and iterating through all postings as the user likes/dislikes the posting.
* Ability to export postings and likes/dislikes (as CSV, PDF, JSON, XLSX, etc.).
* Run on cloud infrastructure instead of locally, likely utilizing Terraform and AWS with the scrapers as a containerized solution running on ECS and the web app running on Amplify or Elastic Beanstalk.
* A matching algorithm that re-sorts postings based on similarity to postings already liked/disliked (likely using key-phrase extraction and the TF-IDF algorithm).
* Incorporation of Glassdoor ratings on the web app job posting card UI component.
* Incorporation of driving distance to a set "home" location on the web app job posting card UI component (likely using a Google API).
* Querying and filtering of postings in the web app.
