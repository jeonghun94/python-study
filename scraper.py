import requests
from bs4 import BeautifulSoup

skills = ["react"]

class JobScraper:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    BASE_URL = "https://berlinstartupjobs.com/skill-areas/"

    def __init__(self, skills):
        self.skills = skills
        self.all_jobs = []
        self.urls = [self.BASE_URL + skill + "/" for skill in self.skills]

    def scrape_jobs(self):
        for url in self.urls:
            print(f"Scraping {url} jobs")
            response = requests.get(url, headers=self.HEADERS)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                self.parse_jobs(soup)
            else:
                print(f"Failed to get {url} jobs")

    def parse_jobs(self, soup):
        job_listings = soup.find_all("li", class_="bjs-jlid")
        for job in job_listings:
            title = job.find("h4", class_="bjs-jlid__h").text.strip()
            company_name = job.find("a", class_="bjs-jlid__b").text.strip()
            description = job.find("div", class_="bjs-jlid__description").text.strip()
            job_link = job.find("h4", class_="bjs-jlid__h").find("a")["href"]

            job_data = {
                "title": title,
                "company": company_name,
                "description": description,
                "url": job_link
            }
            self.all_jobs.append(job_data)

    def get_jobs(self):
        return self.all_jobs



scraper = JobScraper(skills)
scraper.scrape_jobs()
jobs = scraper.get_jobs()

print(jobs)
