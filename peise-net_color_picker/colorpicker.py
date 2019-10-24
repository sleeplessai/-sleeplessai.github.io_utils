import requests
from requests.exceptions import HTTPError
from lxml import html
import os
from time import sleep

# Change DEBUG value to False to collect the whole colors
DEBUG = True

# Task constants
kMaxPageNum = 2 if DEBUG else 23
kBaseUrl = r'http://www.peise.net/color/'
kHtmlPages = [str(i) + '.html' for i in range(1, kMaxPageNum, 1)]
kDownloadDir = r'./color_pages/'
kCollectionFile = r'collected.html'

def Clean():
  print(f'* DEBUG is {DEBUG}.', 'Clean.' if not DEBUG else 'Skip clean.')
  if DEBUG: return
  if os.path.exists(kDownloadDir):
    # directly try to delete all files on dir
    dl_files = os.listdir(kDownloadDir)
    for f in dl_files:
      os.remove(kDownloadDir + f)
  else:
    os.mkdir(kDownloadDir)
  if os.path.exists(kCollectionFile):
    os.remove(kCollectionFile)
  print('* Finish clean.')


def GetPages(need_to_save=False, interval_sec=0.2):
  coll_color_count = 0
  coll_file_ptr = None
  if not need_to_save:
    coll_file_ptr = open(kCollectionFile, 'ab')
  for page in kHtmlPages:
    response = None
    try: 
      response = requests.get(kBaseUrl + page)
      print(f'-> Getting {page}')
      response.raise_for_status()
      print(f'-> Got {page} response.')
      if need_to_save:
        print(f'-> Saving {page}.')
        with open(kDownloadDir + page, 'wb') as f:
          f.write(response.content)
      else:
        print(f'-> Collecting {page}.')
        coll_color_count += CollectColor(response, coll_file_ptr)
    except HTTPError as http_err:
      print(f'-> HTTPError: {http_err}.')
    except Exception as exceptn:
      print(f'-> Exception: {exceptn}.')
    sleep(interval_sec if interval_sec >= 0.2 else 0.2)
  print(f'* Collected-color count: {coll_color_count}.')
  response.close()
  if not need_to_save: coll_file_ptr.close()
  print('* Finish getting pages.')


def CollectColor(response, file_ptr):
  tree = html.fromstring(response.content)
  color_bar_ul_elem = tree.xpath('//*[@id="main"]/div[2]/div[1]/ul/*[@class="indexcolor"]')
  for li in color_bar_ul_elem:
    file_ptr.write(html.tostring(li))
  return len(color_bar_ul_elem)

if __name__ == '__main__':
  Clean()
  GetPages(need_to_save=False)
  # TODO: The file collected.html after collecting does not show color bars. Fix it.
  