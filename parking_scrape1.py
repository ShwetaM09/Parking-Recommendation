# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 12:19:38 2022

@author: Shweta
"""

from datetime import datetime
import time, requests, pandas, lxml
from lxml import html
import json


class Parking_Data:
    
    def CarparksSpider():
        name = "carparks"
        allowed_domains = ["https://en.parkopedia.com/"]
        start_urls = ['https://en.parkopedia.com/parking/locations/northeastern_university_360_huntington_ave_boston_massachusetts_02115_united_states_1ej1drt2y7dwxrh8fb/?arriving={0}&leaving={1}']
                      #'https://en.parkopedia.com/parking/locations/snell_library_360_huntington_ave_boston_massachusetts_02115_united_states_hi56drt2y77xnjrjb7/']
    
    def subdomain(start,end):    
        """
    	This method takes the start and end date (seconds format) and
        symbol(Crypto Currency input by user) and uses this to create the subdomain
        of the URL used for API Call.
        
        Returns - subdomain URL
    	"""
        subdoma="parking/locations/northeastern_university_360_huntington_ave_boston_massachusetts_02115_united_states_1ej1drt2y7dwxrh8fb/?arriving={0}&leaving={1}"
        return subdomain
    
    def header_function(subdomain):
            """
        	Creates header used for API call to yfinance for the historic price data.
            
            Returns - hdrs (header details)
        	"""
            hdrs =  {"authority": "https://en.parkopedia.com/",
                      "method": "GET",
                      "path": subdomain, #path key assigned as subdomain
                      "scheme": "https",
                      "accept": "text/html",
                      "accept-encoding": "gzip, deflate, br",
                      "accept-language": "en-US,en;q=0.9",
                      "cache-control": "no-cache",
                      "cookie": "Cookie:identifier",
                      "dnt": "1",
                      "pragma": "no-cache",
                      "sec-fetch-mode": "navigate",
                      "sec-fetch-site": "same-origin",
                      "sec-fetch-user": "?1",
                      "upgrade-insecure-requests": "1",
                      "user-agent": "Chrome/5.0 (Windows NT 11.0; Win64)"}
            return hdrs
        
    def scrape_page(url, header):
        """
    	Sends request to yfinance with the url and header data and receives the 
        data in html format which is parsed and converted to table format.
        
        Returns - dataframe of the requested info.
    	"""
        pan = requests.get(url,headers=header)
        element_html = html.fromstring(pan.content)
        table = element_html.xpath('//table')
        table_tree = lxml.etree.tostring(table[0], method='xml')
        panda = pandas.read_html(table_tree)
        return panda
        

if __name__ == "__main__": 
    start= str(input('Enter start date & time (yyyy-mm-dd hh:mm): ')) #2022-04-14 18:22
    end= str(input('Enter end date & time (yyyy-mm-dd hh:mm): ')) #2022-04-15 18:22
    subdomain=Parking_Data.subdomain(start,end)
    r=Parking_Data.header_function(subdomain)
    base_url = 'https://en.parkopedia.com/'
    url = base_url + subdomain
    data=Parking_Data.scrape_page(url,r)