#!/usr/bin/env python3

# prepare_data.py requires the following files:
# data/raw/total-final-energy-consumption.csv ( https://data.london.gov.uk/dataset/total-energy-consumption-borough )
# data/raw/hxxvxx_006_2015xxx.tif (these are preprocessed data files)

# prepare_data.py processes the raw data files and converts these to json
# files
import csv
import json
import os
import re
import shutil
from datetime import datetime
from PIL import Image

if not os.path.exists('www/data/'):
  os.makedirs('www/data/')

with open('data/raw/total-final-energy-consumption.csv') as csvfile:
  print('Converting total-final-energy-consumption.csv')

  csv_reader = csv.DictReader(csvfile)
  observations = []

  for row in csv_reader:
    observation = {
      'area': row['Area'],
      'year': row['Year'],
      'value': row['Value']
    }

    observations.append(observation)

  with open('www/data/energy_consumption.json', 'w') as jsonfile:
    json.dump(observations, jsonfile)

print("Done")

print('Converting surface temperature files')
surf_temp_dir = 'data/raw/surface_temperature/'
png_files = []
for filename in os.listdir(surf_temp_dir):
  if filename[-3:] != 'tif':
    continue

  tif_path = surf_temp_dir + filename
  meta_file_path = surf_temp_dir + filename + '.aux.xml'

  png_path = 'www/data/' + filename[:-3] + "png"
  tiffile = Image.open(tif_path)
  pngfile = tiffile.convert('RGBA')
  pngfile.save(png_path, 'PNG')

  production_date_line_id, production_date = None, None
  north_coordinate_line_id, north_coordinate = None, None
  east_coordinate_line_id, east_coordinate = None, None
  south_coordinate_line_id, south_coordinate = None, None
  west_coordinate_line_id, west_coordinate = None, None

  if os.path.exists(meta_file_path):
    with open(meta_file_path) as metafile:
      lines = metafile.readlines()
      for line_id, line in enumerate(lines):
        if re.match(r'\s+OBJECT\s*=\s*PRODUCTIONDATETIME', line):
          production_date_line_id = line_id + 2
        if re.match(r'\s+OBJECT\s*=\s*NORTHBOUNDINGCOORDINATE', line):
          north_coordinate_line_id = line_id + 2
        if re.match(r'\s+OBJECT\s*=\s*EASTBOUNDINGCOORDINATE', line):
          east_coordinate_line_id = line_id + 2
        if re.match(r'\s+OBJECT\s*=\s*SOUTHBOUNDINGCOORDINATE', line):
          south_coordinate_line_id = line_id + 2
        if re.match(r'\s+OBJECT\s*=\s*WESTBOUNDINGCOORDINATE', line):
          west_coordinate_line_id = line_id + 2

        if line_id == production_date_line_id:
          production_date = (line.split('= ')[1]).strip()
        if line_id == north_coordinate_line_id:
          north_coordinate = float((line.split('= ')[1]).strip())
        if line_id == east_coordinate_line_id:
          east_coordinate = float((line.split('= ')[1]).strip())
        if line_id == south_coordinate_line_id:
          south_coordinate = float((line.split('= ')[1]).strip())
        if line_id == west_coordinate_line_id:
          west_coordinate = float((line.split('= ')[1]).strip())
  
  if production_date is None:
    production_date = str(datetime.now())

  png_files.append({
    'filename': png_path[4:],
    'north_bound': north_coordinate,
    'east_bound': east_coordinate,
    'south_bound': south_coordinate,
    'west_bound': west_coordinate,
    'production_datetime': production_date
  })

with open('www/data/temperature_data.json', 'w') as jsonfile:
  json.dump(png_files, jsonfile)
print("Done")

print('Copying shape files')
shape_dir = 'data/raw/shapes/'
shape_files = []
for filename in os.listdir(shape_dir):
  if filename[-7:] != 'geojson':
    continue
  shape_files.append(filename)
  shutil.copyfile(shape_dir + filename, 'www/data/' + filename)
with open('www/data/shape_data.json', 'w') as jsonfile:
  json.dump(shape_files, jsonfile)
print("Done")