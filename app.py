from flask import Flask, render_template, request
from scraper import JobScraper

app = Flask("JobScraper")
db = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search") 
def search():
    keyword = request.args.get("keyword")

    if keyword in db:
        jobs = db[keyword]

    else:
        scraper = JobScraper(keyword)
        scraper.scrape_jobs()
        jobs = scraper.get_jobs()
        db[keyword] = jobs

    return render_template("search.html", keyword=keyword, jobs=jobs)

app.run("127.0.0.1",port=3000, debug=True)