# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 16:37:47 2022

@author: Shweta Mishra
"""
import requests
import json
from lxml import html
import pandas as pd

class Parking_Data:
    
    def subdomain(start,end):    
        """
    	This method takes the start and end date (yyyymmddhhmm)  and uses this to create the subdomain
        of the URL used for API Call.
        
        Returns - subdomain URL
    	"""
        subdoma="parking/locations/northeastern_university_360_huntington_ave_boston_massachusetts_02115_united_states_1ej1drt2y7dwxrh8fb/?arriving={0}&leaving={1}"
        return subdoma
    
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
        items = []
        pan = requests.get(url,headers=header)
        element_html = html.fromstring(pan.content)
        data = element_html.xpath("//div [@id='App']/div/@data-react-props")
        carparks = json.loads(data[0])['locations']['all']
        #print(carparks)
        
        for item in carparks:
            distance=500
            if 'distance' in item['properties']:
                if item['properties']['distance'] <=distance:
                    if 'name' in item['properties']:
                        name = item['properties']['name']
                    else:
                        name = "-"
                    if 'capacity' in item['properties']:
                        capacity = item['properties']['capacity']
                    else:
                        capacity = 1
                    if 'prices' in item['properties']:
                        cost = item['properties']['prices']['entries'][0]['costs'][0]['amount_text_encoded']
                    else:
                        cost = "$10"
                    if 'distance' in item['properties']:
                        distance = item['properties']['distance']
                    else:
                        distance = "-"
                    if 'city' in item['properties']:
                        city = item['properties']['city']
                    else:
                        city = "-"
                        
                    if 'geometries' in item['geometry']:
                        area = item['geometry']['geometries'][0]['coordinates']
                    else:
                        area = "-"    
                    items.append((name,city,distance,cost,area))
                else:
                    pass
        y=pd.DataFrame(items)
        y.to_excel("PS1.xlsx", sheet_name="nodes", index=False)
        return 0

if __name__ == "__main__": 
    start= str(input('Enter start date & time (yyyy-mm-dd hh:mm): ')) #2022-04-14 18:22
    end= str(input('Enter end date & time (yyyy-mm-dd hh:mm): ')) #2022-04-15 18:22
    subdomain=Parking_Data.subdomain(start,end)
    r=Parking_Data.header_function(subdomain)
    base_url = 'https://en.parkopedia.com/'
    url = base_url + subdomain
    data=Parking_Data.scrape_page(url,r)