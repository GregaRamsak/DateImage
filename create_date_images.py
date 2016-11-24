#!/usr/bin/env python3

from PIL import Image  # cmd> pip install image
from datetime import datetime
from os import listdir, remove
from os.path import isfile, join
import fileinput
import subprocess
import tempfile

## --- Functions --- ##

def get_date_taken_from_img( path, showTime = False ):
  imgDate = Image.open(path)._getexif()[36867] # Date Created
  return datetime.strptime(imgDate, '%Y:%m:%d %H:%M:%S').strftime('%d.%m.%Y %H.%M.%S' if showTime else '%d.%m.%Y')

def get_svg_template():
  # Read SVG file
  with open('date_template.svg', 'r') as svgTemplateFile:
      content = svgTemplateFile.read().replace('\n', '')
  return content

def create_date_images( date, content ):
  filesToDelete = []
  
  # Replace date in file
  content_with_date = content.replace("%date%", date)

  # Save to file
  with tempfile.NamedTemporaryFile( mode='w', delete=False ) as f:
    f.write(content_with_date)
    f.flush()

    # Export to PNG
    subprocess.call(['inkscape', f.name, '--export-png=date_{0}.png'.format(date)])

    filesToDelete.append(f.name)
  # / with

  # Delete temp file
  for fileToDel in filesToDelete:
    remove(fileToDel)

## --- Functions --- ## End

mypath = 'img/'

for filepath in [f for f in listdir(mypath) if isfile(join(mypath, f))]:
  print(mypath + filepath);
  create_date_images(get_date_taken_from_img(mypath + filepath), get_svg_template());

print('Done!');
