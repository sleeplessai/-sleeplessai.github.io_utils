import pathlib
from ip import ImageProperty
from pit import PostImageTool as pit

def get_post_images(post):
  image_props = []
  with open(post, encoding='utf-8') as post_md:
    line_num = 0
    for line in post_md:
      line_num += 1
      if pit.is_md_image(line):   # regex for md image
        hint, url, fmt = pit.resolve_md_image(line)
        ip = ImageProperty(post.name[:-3], line_num, hint, url, fmt)
        image_props.append(ip)
      else:
        pass  # if needed
  return image_props

def main():
  # argparser.. if needed
  constltn_local = '../../sleeplessai.github.io/_posts'
  constltn_path = pathlib.Path(constltn_local)
  post_md_files = list(constltn_path.glob('*.md'))
  image_backup_to = './post_images'
  for md in post_md_files:
    md_base_name = md.name.replace('.md', '')
    img_dir_path = pathlib.Path(image_backup_to, md_base_name)
    pit.make_post_folder(img_dir_path)
    image_props = get_post_images(md)
    for i in image_props:
      print(i.as_json())
      pit.download_image(i.as_dict(), base=image_backup_to)
    pit.dump_image_prop_list(image_props, pathlib.Path(img_dir_path, md_base_name + '.json'))

if __name__ == '__main__':
  main()