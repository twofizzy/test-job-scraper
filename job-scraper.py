import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
import re

URL = "https://jobs.arts.ac.uk/vacancies/"

def scrape_jobs():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}) # does this remain the same each time or differ for each site?
    
    soup = BeautifulSoup(r.text, "html.parser")
    jobs = []

    for card in soup.select("a[href*='/job/']"):
        title_el = card.select_one("h3, h2")
        if not title_el:
            continue
        title = title_el.get_text(strip=True)
        link = card["href"]
        if not link.startswith("http"):
            link = "https://jobs.arts.ac.uk" + link

        salary_el = card.select_one("strong")
        salary = salary_el.get_text(strip=True) if salary_el else ""

        jobs.append({"title": title, "link": link, "salary": salary})

    return jobs

def generate_feed(jobs):
    fg = FeedGenerator()
    fg.id(URL)
    fg.title("UAL Jobs Feed")
    fg.link(href=URL, rel="alternate")
    fg.description("Latest jobs from UAL")

    for job in jobs:
        fe = fg.add_entry()
        fe.id(job["link"])
        fe.title(job["title"])
        fe.link(href=job["link"])
        fe.description(f"Salary: {job['salary']}")
        fe.published(datetime.now(timezone.utc))

    fg.rss_file("ual_jobs.xml")
    print(f"Feed written with {len(jobs)} jobs.")

jobs = scrape_jobs()
generate_feed(jobs)