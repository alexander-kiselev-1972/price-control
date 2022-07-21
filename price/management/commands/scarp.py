import urllib.request as web
from bs4 import BeautifulSoup
import re
import zipfile
import os
import schedule
import time
from pathlib import Path


def scarp2():
    link_div = ""
    try:
        page = web.urlopen('https://grls.rosminzdrav.ru/pricelims.aspx')
        soup = BeautifulSoup(page, 'html.parser')
        link_div = soup.find(id="ctl00_plate_tdzip")
    except:
        pass

    return link_div.a["href"]

def url_file(s):
    url_file = 'https://grls.rosminzdrav.ru/' + s
    return url_file

def download_file(url_file):
    f = web.urlopen(url_file)
    return f


def razarch(f):
    with open("code2.zip", "wb") as code:
        code.write(f.read())
    fantasy_zip = zipfile.ZipFile("code2.zip")
    fantasy_zip.extractall('files')
    fantasy_zip.close()


# def scraper_web():
#     time.sleep(10)
#     page = None
#
#     while page == None:
#         try:
#             page = web.urlopen('https://grls.rosminzdrav.ru/pricelims.aspx')
#
#             print("17 row it's ok")
#         except Exception as e:
#             print("Error: ", e)
#
#     soup = BeautifulSoup(page, 'html.parser')
#     try:
#         link_div = soup.find(id="ctl00_plate_tdzip")
#         s = link_div.a["href"]
#     except:
#         pass
#     try:
#
#         url_file = 'https://grls.rosminzdrav.ru/' + s
#
#         f = web.urlopen(url_file)
#         time.sleep(45)
#         with open("code2.zip", "wb") as code:
#             code.write(f.read())
#
#         print("38 row it's ok")
#     except Exception as e:
#         print("error: ", e)
#
#     # p = re.compile(r"GetLimPrice\.ashx\?FileGUID=[\w{1,}-]*\w{1,}&UserReq=[0-9]*", re.I)
#     #
#     # for link in soup.find_all('a'):
#     #     s = link.get('href')
#     #     print(s, "in for. 28 line ")
#     #
#     #     #
#     #     if p.search('{}'.format(s)):
#     #         print("row", 32)
#     #         time.sleep(7)
#     #         f = None
#     #         while f == None:
#     #             try:
#     #                 print(s)
#     #                 url_file = 'https://grls.rosminzdrav.ru/' + s
#     #
#     #                 f = web.urlopen(url_file)
#     #
#     #                 print("38 row it's ok")
#     #             except Exception as e:
#     #                 print("error: ", e)
#
#
#
#     fantasy_zip = zipfile.ZipFile("code2.zip")
#     fantasy_zip.extractall('files')
#     fantasy_zip.close()


def get_filepaths(directory):
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.


def runter():
    link_div = scarp2()
    k = url_file(link_div)
    d = download_file(k)
    razarch(d)
    a = get_filepaths('files')
    for file in a:
        g = file
        os.rename(str(g), 'files/1.xls')





while os.path.exists('files/1.xls') == False:
    runter()
# s = os.path.exists('files/1.xls')
# print(s)