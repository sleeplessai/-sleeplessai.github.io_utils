import pathlib
from utils import is_md_image, resolve_md_image, make_post_folder, download_image, ImageProperty

constltn_local = '../../sleeplessai.github.io/_posts'
constltn_path = pathlib.Path(constltn_local)
post_md_files = list(constltn_path.glob('*.md'))
image_backup_to = './'

def get_post_images(post):
  image_urls = []
  with open(post, encoding='utf-8') as post_md:
    line_num = 0
    for line in post_md:
      line_num += 1
      if is_md_image(line):   # regex for md image
        hint, url, fmt = resolve_md_image(line)
        ip = ImageProperty(post.name[:-3], line_num, hint, url, fmt).as_dict()
        image_urls.append(ip)
      else:
        pass  # if needed
  return image_urls

for md in post_md_files:
  make_post_folder(md.name.replace('.md', ''))
  li = get_post_images(md)
  for i in li:
    print(i)
    download_image(i)
    