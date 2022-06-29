from pkgutil import get_data
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os

from sympy import div

class linkedin_jobs:
    def __init__(self,keyword, location, pg_num = 0,position = 1):
        self.keyword = keyword
        self.pg_num = pg_num
        self.position = position
        self.location = location
    
    def set_url(self):
        return f"https://www.linkedin.com/jobs/search?keywords={self.keyword}&location={self.location}&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position={self.position}&pageNum={self.pg_num}"
        
    def make_request(self):
        url = self.set_url()
        return requests.get(url)
    
    def get_data(self):
        r = self.make_request()
        soup = BeautifulSoup(r.content, 'lxml')
        return(soup)

    def info(self):
        data = self.get_data()
        div_tag = data.findAll('div', {"class":'base-search-card__info'})
        job_titles =[]
        company_name =[]
        location =[]

        for job in div_tag:
            job_titles.append(job.find('h3').text)
            company_name.append(job.find('h4').text)
            location.append(job.find('span').text)

        div = data.findAll('div', {'class':'base-card'})
        url = []
        for item in div: 
            url.append(item.a['href'])

        jobs = pd.DataFrame({
            'Job Title': job_titles,
            'company_name': company_name,
            'location': location,
            'URL': url
        })
        return(jobs)

    def store_content(self,name):
        data = self.info()
        data.to_csv("job.csv")


    def Scrapper(self,positions):
        for position in range(0,positions+1):
            self.get_data()
            self.store_content('job')
            self.position += 1

if __name__ == "__main__":
    scrapper = linkedin_jobs("Data Analyst", "Ontario")
    scrapper.Scrapper(1)