#!/usr/bin/python

from BeautifulSoup import BeautifulSOAP

import urllib2
import subprocess
import logging
import os

BASE_URL = "http://www.podnapisi.net"
BASE_SEARCH = BASE_URL + "/he/" + "ppodnapisi/search?sK="

# TODO get this information from the user
SERIES_NAME = "mad men"
SEASON = 2
EPISODE = 6


def download_subtitle(series_name, season, episode):
    """

    :param series_name:
    :param season:
    :param episode:
    """
    dir_name = "{}_s{:02}e{:02}".format(series_name, season, episode)
    if not os.access(dir_name, os.F_OK):
        os.mkdir(dir_name)
    os.chdir(dir_name)
    search_url = "{}{} s{:02}e{:02}".format(BASE_SEARCH, series_name, season, episode).replace(" ", "+")
    logging.info("Search url: {}".format(search_url))
    search_page_data = BeautifulSOAP(urllib2.urlopen(search_url).read())

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
        zip_filename = "{}.zip".format(i)
        open(zip_filename, "wb").write(download_data)
        subprocess.call(["unzip", zip_filename])
        logging.info("Unzipped {}".format(zip_filename))
        os.unlink(zip_filename)

if __name__ == "__main__":
    download_subtitle(SERIES_NAME, SEASON, EPISODE)
