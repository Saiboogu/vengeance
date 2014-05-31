#!/usr/bin/env python
from time import sleep
from bs4 import BeautifulSoup
import re
import requests
import json

posters = []
baseurl = "http://www.mondotees.com/"
edition_regex = re.compile(r'Edition of (\d+)')

while True:
  request = requests.get(baseurl)
  main_soup = BeautifulSoup(request.text)
  available =\
    [baseurl+a.get("href") for a in main_soup.find("ul").findAll("a")]

  if posters != []:
    oldposters = posters

  posters = []

  for url in available:
    new_soup = BeautifulSoup(requests.get(url).text)
    poster = {
      "available": new_soup.find(id="availability").text.find("Sold Out") < 0,
      "url": url,
      "price": new_soup.find(class_="price").text,
      "title": new_soup.find(class_="page_headers").text,
    }

    try:
      poster["editionof"] =\
        int(edition_regex.findall(new_soup.find(class_="item").text)[0])
    except:
      pass

    posters.append(poster)
  
  print json.dumps(posters, indent=2)
  sleep(30)
