#!/usr/bin/python

from BeautifulSoup import BeautifulSOAP

import urllib2
import subprocess
import logging

BASE_URL = "http://www.podnapisi.net"
BASE_SEARCH = BASE_URL + "/he/" + "ppodnapisi/search?sK="

SERIES_NAME = "mad men"
SEASON = 2
EPISODE = 5

search_url = "{}{} s{:02}e{:02}".format(BASE_SEARCH, SERIES_NAME, SEASON, EPISODE).replace(" ", "+")
logging.info("Search url: {}".format(search_url))
search_page_data = BeautifulSOAP(urllib2.urlopen(search_url).read())
search_results = search_page_data.findAll(attrs={"class": "subtitle_page_link"})
search_results_table = search_page_data.find(attrs={"class": "list first_column_title"})
results = search_results_table.tbody.findAll("tr")
results = [x for x in results if x.findAll("td")[2].a.div["alt"] == "English subtitles"]
results = [x.findAll("td")[0].findAll("div")[1].a["href"] for x in results]

for i, result in enumerate(results):
    download_page_url = BASE_URL + "/he/" + result
    download_page_data = urllib2.urlopen(download_page_url).read()
    download_button = BeautifulSOAP(download_page_data).find(attrs={"class": "button big download"})
    download_url = BASE_URL + download_button.get("href")
    download_data = urllib2.urlopen(download_url).read()
    zip_filename = "{} {} s{:02}e{:02}.zip".format(i, SERIES_NAME, SEASON, EPISODE)
    open(zip_filename, "wb").write(download_data)
    subprocess.call(["unzip", zip_filename])
    logging.info("Unzipped {}".format(zip_filename))
