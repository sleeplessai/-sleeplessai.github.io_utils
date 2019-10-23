import requests
from requests.exceptions import HTTPError
from lxml import html
import os

# Change DEBUG value to False to collect the whole colors
DEBUG = True

# Task constants
kMaxPageNum = 2 if DEBUG else 23
kBaseUrl = r'http://www.peise.net/color/'
kHtmlPages = [str(i) + '.html' for i in range(1, kMaxPageNum, 1)]
kDownloadDir = r'./peise_net/'
kCollectionFile = r'collected.html'

def Clean():
  pass
  # TODO: remove download dir forcely
  # if os.path.exists(kDownloadDir):
  #   os.removedirs(kDownloadDir)
  # os.mkdir(kDownloadDir)
  # if os.path.exists(kCollectionFile):
  #   os.remove(kCollectionFile)


def GetPages(need_to_save=False):
  if not need_to_save:
    if os.path.exists(kCollectionFile):
      os.remove(kCollectionFile)
    coll_file_ptr = open(kCollectionFile, 'ab')
    coll_color_count = 0
  
  for page in kHtmlPages:
    try: 
      response = requests.get(kBaseUrl + page)
      print(f'Visiting {page}')
      response.raise_for_status()
    except HTTPError as http_err:
      print(f'HTTPError: {http_err}')
    except Exception as exceptn:
      print(f'Exception: {exceptn}')
    finally:
      print('Visiting Ok.')
      if need_to_save:
        print(f'Saving {page}')
        with open(kDownloadDir + page, 'wb') as f:
          f.write(response.content)
      else:
        print(f'Collecting {page}')
        coll_color_count += CollectColor(response, coll_file_ptr)

  print(f'Collected-color count: {coll_color_count}')
  response.close()
  coll_file_ptr.close()


def CollectColor(response, file_ptr):
  tree = html.fromstring(response.content)
  color_bar_ul_elem = tree.xpath('//*[@id="main"]/div[2]/div[1]/ul/*[@class="indexcolor"]')
  for li in color_bar_ul_elem:
    file_ptr.write(html.tostring(li))
  return len(color_bar_ul_elem)


if __name__ == '__main__':
  if not DEBUG:
    Clean()
  GetPages()
