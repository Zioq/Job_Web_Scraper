import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://ca.indeed.com/jobs?q=python&limit={LIMIT}"


def get_last_page():
    # Get the HTML Text
    result = requests.get(URL)

    # Extract data from HTML
    soup = BeautifulSoup(result.text, "html.parser")

    # Find div which is a <div class="pagination"> to see how many pages have
    pagination = soup.find("div", {"class": "pagination"})

    # Find all anchors in pagination
    links = pagination.find_all('a')

    pages = []
    # Find all spans in anchor lists `string` data
    # Remove unnecessary last element
    for link in links[:-1]:
        pages.append(int(link.string))  # convert string to Int

    max_page = pages[-1]
    return max_page


def extract_company(html):
    # chaining
    title = (html.find("h2", {"class": "title"})).find("a")["title"]

    # Get company title
    company = html.find("span", {"class": "company"})
    company_anchor = company.find("a")
    if company:

        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
        company = company.strip()  # Delete white space
    else:
        company = None
    # Get the location
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]

    # Get job Id
    job_id = html["data-jk"]
    #print(job_id)


    return {'title': title, 'company': company, 'location': location, 'link': f"https://ca.indeed.com/jobs?q=python&vjk={job_id}"}


def extract_jobs(last_page):
    jobs = []

    # for page in range(last_page):
    for page in range(last_page):
        print(f"Scraping page: {page}")
        result = requests.get(f"{URL}&startstart={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            ''' title = (result.find("h2",{"class":"title"}))
            anchor = title.find("a")["title"] '''
            job = extract_company(result)
            jobs.append(job)

    return jobs

def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
