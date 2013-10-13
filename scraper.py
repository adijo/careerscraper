from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen


class companyDownloader(object):
    """Takes a company name as an input and downloads all associated questions from careercup.com"""
    def __init__(self,company_name):
        self.raw_url = "http://www.careercup.com/page?pid="
        self.company_url = ""
        pieces = company_name.split(" ")
        for piece in pieces:
            self.company_url += piece + "-"
        self.final_url = self.raw_url + self.company_url + "interview-questions"
        
    def page_scraper(self,url):
        try:
            self.text = urlopen(url)
        except:
            raise Exception("Not a valid company name.")
        self.soup = BeautifulSoup(self.text.read())
        return self.soup.findAll("span","entry")


