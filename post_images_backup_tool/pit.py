# pit: post image toolkit
import requests
import re
import pathlib
import json
from os import mkdir
from time import sleep
from ip import ImageProperty

class PostImageTool(object):
  @staticmethod
  def is_md_image(md_line):
      return re.match(r'!\[[^\]]+\]\([^\)]+\)', md_line)

  @staticmethod
  def resolve_md_image(md_line):
    # string between [] and () re
    hint_re = re.compile(r'[\[](.*?)[\]]')
    url_re = re.compile(r'[(](.*?)[)]')
    hint = re.findall(hint_re, md_line)[0]
    url = re.findall(url_re, md_line)[0]
    fmt = ''
    for i in url[::-1]:
      if i == '.': break
      fmt += i
    fmt = fmt[::-1]
    return hint, url, fmt

  @staticmethod
  def __download_image(src, dst):
    headers = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'accept-encoding': 'gzip, deflate, br',
      'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
      'cache-control': 'max-age=0',
      'dnt': '1',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'cross-site',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    # chunk ref: https://blog.csdn.net/qq_34504481/article/details/79716106
    r = requests.get(src, stream=True, headers=headers)
    with open(dst, 'wb') as f:
      for chunk in r.iter_content(chunk_size=32):
        f.write(chunk)

  @classmethod
  def download_image(cls, ip, base='./', slp=1.0):
    dst_name = 'line_' + str(ip['line_num']) + '-' + ip['hint'] + '.' + ip['fmt']
    dst_path = pathlib.Path(base, ip['post'], dst_name)
    cls.__download_image(ip['url'], dst_path)
    sleep(slp)

  @staticmethod
  def make_post_folder(post):
    try:
      mkdir(post)
    except:
      pass
  
  @staticmethod
  def dump_image_prop_list(ip, dst='./curr_post_image.json'):
    _ip = ip
    if isinstance(ip, list):
      if len(ip) and isinstance(ip[0], ImageProperty): 
        _ip = [x.as_dict() for x in ip]
    elif isinstance(ip, ImageProperty):
      _ip = [].append(ip.as_dict())
    with open(dst, 'w') as f:
      json.dump(_ip, f, ensure_ascii=False, indent=2)
