import zipfile
import requests
import doubleagent
from bs4 import BeautifulSoup
from selenium import webdriver
import sys
import os


def CrhomedriverUpdate(ex):

    ex = str(ex)
    version = ex.split('Current browser version is ')[1]
    version = version.split(' with')[0]

    versionNumber = version.split('.')[:-1]
    versionNumber = ".".join(versionNumber)

    res = requests.get(
        'https://sites.google.com/a/chromium.org/chromedriver/downloads').text

    soup = BeautifulSoup(res, 'html.parser')
    link = soup.find_all('a')
    chromeUrlraw_list = []
    for li in link:
        li_raw = li.prettify()

        if 'https://chromedriver.storage.googleapis.com/index.html?path' in li_raw:
            chromeUrlraw_list.append(li_raw.split('"')[1])

    for chromeUrlraw in chromeUrlraw_list:

        chromeUrlraw = chromeUrlraw.split(
            'https://chromedriver.storage.googleapis.com/index.html?path=')[1][:-1]
        chromeUrl = chromeUrlraw.split('.')[:-1]
        chromeUrl = ".".join(chromeUrl)
        if chromeUrl == versionNumber:

            break

    download = requests.get(
        'https://chromedriver.storage.googleapis.com/'+str(chromeUrlraw)+'/chromedriver_win32.zip')
    file = open('zip.zip', 'wb')
    file.write(download.content)
    file.close()

    fantasy_zip = zipfile.ZipFile('zip.zip')
    fantasy_zip.extractall('./')

    fantasy_zip.close()
    os.remove('zip.zip')
