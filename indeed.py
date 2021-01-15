import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://ca.indeed.com/jobs?q=python&limit={LIMIT}"

def extract_indeed_pages():
    #Get the HTML Text
    result = requests.get(URL)

    #Extract data from HTML 
    soup = BeautifulSoup(result.text, "html.parser")

    # Find div which is a <div class="pagination"> to see how many pages have
    pagination = soup.find("div",{"class":"pagination"})

    # Find all anchors in pagination
    links = pagination.find_all('a')

    pages = [] 
    # Find all spans in anchor lists `string` data
    #Remove unnecessary last element
    for link in links[:-1]: 
        pages.append(int(link.string)) #convert string to Int

    max_page = pages[-1]
    return max_page

def extract_indeed_jobs(last_page):
    jobs = []

    #for page in range(last_page):
    result = requests.get(f"{URL}&startstart={0*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results =soup.find_all("div",{"class":"jobsearch-SerpJobCard"})
    for result in results:
        ''' title = (result.find("h2",{"class":"title"}))
        anchor = title.find("a")["title"] '''
        
        #chaining 
        title = (result.find("h2",{"class":"title"})).find("a")["title"]
        print(title)
    return jobs