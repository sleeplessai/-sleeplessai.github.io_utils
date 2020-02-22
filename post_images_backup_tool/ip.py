# ip: image property
import json

class ImageProperty(object):
  def __init__(self, post, line_num, hint, url, fmt):
    self.post = post
    self.line_num = line_num
    self.hint = hint
    self.url = url
    self.fmt = fmt
  
  def as_dict(self):
    return {
      'post': self.post,
      'line_num': self.line_num,
      'hint': self.hint,
      'url': self.url,
      'fmt': self.fmt
    }

  def as_json(self, indent=2):
    return json.dumps(self.as_dict(), indent=indent)