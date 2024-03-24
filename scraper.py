import requests
from bs4 import BeautifulSoup

class JobScraper:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    def __init__(self, skill):
        self.skill = skill
        self.all_jobs = []

    def fetch_and_parse(self, url, parser_method):
        response = requests.get(url, headers=self.HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            parser_method(soup)
        else:
            print(f"{url}에서 작업 공고를 가져오는 데 실패했습니다.")

    def scrape_jobs(self):
        self.fetch_and_parse(f"https://berlinstartupjobs.com/skill-areas/{self.skill}/", self.parse_jobs)
        self.fetch_and_parse(f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={self.skill}", self.parse_jobs_wwr)
        self.fetch_and_parse(f"https://web3.career/{self.skill}-jobs", self.parse_jobs_web3)

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
                "site": "berlinstartupjobs",
                "url": job_link
            }
            self.all_jobs.append(job_data)
        pass

    def parse_jobs_web3(self, soup):
        job_listings = soup.find_all("tr", class_="table_row")
        for job in job_listings:
            title = job.find("div", class_="align-middle").text.strip()
            company = job.find("td", class_="job-location-mobile").text.strip()
            description = 'no description available'
            url_str =   job.find("div", class_="job-title-mobile").find("a")["href"]
            url = f"https://web3.career/{url_str}"

            job_data = {
                "title": title,
                "company": company,
                "description": description,
                "site": "web3",
                "url": url
            }
            self.all_jobs.append(job_data)    
        pass

    def parse_jobs_wwr(self, soup):
        job_listings = soup.find_all("li", class_="feature")
        for job in job_listings:
            title = job.find("span", class_="title").text.strip()
            company = job.find("span", class_="company").text.strip()
            description = job.find("span", class_="region").text.strip()
            url_str = job.find_all("a")
            url = f"https://weworkremotely.com{url_str[1]['href'] if len(url_str) > 1 else url_str[0]['href']}"
            
            job_data = {
                "title": title,
                "company": company,
                "description": description,
                "site": "weworkremotely",
                "url": url
            }
            self.all_jobs.append(job_data)  
        pass

    def get_jobs(self):
        self.scrape_jobs()  
        return self.all_jobs
