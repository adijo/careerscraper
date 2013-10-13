from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import shelve
import unicodedata

class companyDownloader(object):
    """Takes a company name as an input and downloads all associated questions from careercup.com"""
    
    def __init__(self,company_name):
        
        self.raw_url = "http://www.careercup.com/page?pid="
        self.company_name = company_name
        self.company_url = ""
        pieces = company_name.split(" ")
        for piece in pieces:
            self.company_url += piece + "-"
        self.final_url = self.raw_url + self.company_url + "interview-questions"
        self.database = shelve.open("database2.txt")
        self.file = open(company_name + ".txt","w")
        self.file.write(company_name.capitalize())
        self.file.write("\n\n\n\n")
        
    def page_scraper(self,url):
        try:
            self.text = urlopen(url)
        except:
            raise Exception("Not a valid company name.")
        self.soup = BeautifulSoup(self.text.read())
        occurences = self.soup.findAll("span","entry")
        
        urls = []
        for url in occurences:
            urls.append(url)
        return urls

    def change_url(self,url):
        return url + "&n=" + str(self.pageNo)

    def travelToURL(self,question_url):
        soup = BeautifulSoup(urlopen(question_url).read())
        #Extract number of votes from the question
        votes = int(soup.find('div',{"class": 'votesNetQuestion'}).contents[0])
        
        if votes >= 0:
            
            if self.company_name not in self.database:
                self.database[self.company_name] = []
            raw_information = soup.find('p').contents
            #Needs better work here.          
            for line in raw_information:
                try:
                    filtered = unicodedata.normalize('NFKD',line ).encode('ascii','ignore')
                    self.file.write(filtered.capitalize())
                except:
                    self.file.write("\n")
            self.file.write("\n\n\n\n")       
            
            
    def span_to_formattedURL(self,span):
        start = span.find("href\=")
        counter = start + 1
        while span[counter] != '"':
            counter += 1
        return "http://www.careercup.com/" + span[start:counter+1]
        
    def driver_method(self):
        list_of_urls = self.page_scraper(self.final_url)
        
        for question in list_of_urls:
            q_url = "http://www.careercup.com" + str(question.contents[1]['href'])
            self.travelToURL(q_url)


d = companyDownloader("epic systems")
d.driver_method()
