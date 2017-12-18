#!/usr/bin/env python3

# prepare_data.py requires the following files:
# data/raw/total-final-energy-consumption.csv ( https://data.london.gov.uk/dataset/total-energy-consumption-borough )
# data/raw/hxxvxx_006_2015xxx.tif (these are preprocessed data files)

# prepare_data.py processes the raw data files and converts these to json
# files
import csv
import json
import numpy
import os
import re
import shutil
from datetime import datetime
from matplotlib import pyplot
from pyhdf.SD import *
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

print('Converting surface temperature files v2')
surf_temp_dir = 'data/raw/surface_temperature_v2/'
png_files = []
for filename in os.listdir(surf_temp_dir):
  if filename[-3:] != 'hdf':
    print('Ignoring ' + filename)
    continue
  hdf_path = surf_temp_dir + filename
  hdf_file = SD(hdf_path)

  # Available datasets:
  #  LST_Day_1km: (('YDim:MODIS_Grid_Daily_1km_LST', 'XDim:MODIS_Grid_Daily_1km_LST'), (1200, 1200), 23, 0)
  #  QC_Day: (('YDim:MODIS_Grid_Daily_1km_LST', 'XDim:MODIS_Grid_Daily_1km_LST'), (1200, 1200), 21, 1)
  #  Day_view_time: (('YDim:MODIS_Grid_Daily_1km_LST', 'XDim:MODIS_Grid_Daily_1km_LST'), (1200, 1200), 21, 2)
  #  Day_view_angl: (('YDim:MODIS_Grid_Daily_1km_LST', 'XDim:MODIS_Grid_Daily_1km_LST'), (1200, 1200), 21, 3)
  #  LST_Night_1km: (('YDim:MODIS_Grid_Daily_1km_LST', 'XDim:MODIS_Grid_Daily_1km_LST'), (1200, 1200), 23, 4)
  #  QC_Night: (('YDim:MODIS_Grid_Daily_1km_LST', 'XDim:MODIS_Grid_Daily_1km_LST'), (1200, 1200), 21, 5)
  #  Night_view_time: (('YDim:MODIS_Grid_Daily_1km_LST', 'XDim:MODIS_Grid_Daily_1km_LST'), (1200, 1200), 21, 6)
  #  Night_view_angl: (('YDim:MODIS_Grid_Daily_1km_LST', 'XDim:MODIS_Grid_Daily_1km_LST'), (1200, 1200), 21, 7)
  #  Emis_31: (('YDim:MODIS_Grid_Daily_1km_LST', 'XDim:MODIS_Grid_Daily_1km_LST'), (1200, 1200), 21, 8)
  #  Emis_32: (('YDim:MODIS_Grid_Daily_1km_LST', 'XDim:MODIS_Grid_Daily_1km_LST'), (1200, 1200), 21, 9)
  #  Clear_day_cov: (('YDim:MODIS_Grid_Daily_1km_LST', 'XDim:MODIS_Grid_Daily_1km_LST'), (1200, 1200), 23, 10)
  #  Clear_night_cov: (('YDim:MODIS_Grid_Daily_1km_LST', 'XDim:MODIS_Grid_Daily_1km_LST'), (1200, 1200), 23, 11)
  hdf_obj = hdf_file.select('LST_Night_1km')

  png_path = 'www/data/' + filename[:-3] + "png"
  data_matrix = numpy.array(hdf_obj.get())

  min_val = min(numpy.array(data_matrix).flatten())
  max_val = max(numpy.array(data_matrix).flatten())

  # low = min(x for x in numpy.array(data_matrix).flatten() if x > min_val)
  # high = max(x for x in numpy.array(data_matrix).flatten() if x < max_val)
  low, high = 12000, 14000 # This seems to be an appropriate range for all images
  print('{} Min: {}, Max {}, Clipping to range ({}, {})'.format(filename, min_val, max_val, low, high))

  image_int_matrix = numpy.clip(data_matrix, low, high)
  image_int_matrix = numpy.divide(numpy.subtract(image_int_matrix, low), high - low)
  image_int_matrix *= 255
  
  img = Image.fromarray(numpy.uint8(image_int_matrix)).convert('RGBA')

  # Set transparency
  col_img = []
  for val in img.getdata():
    intensity = val[0]
    opacity = 255
    if intensity == 0:
      opacity = 0
    col_img.append((intensity, 0, 0, opacity))
  img.putdata(col_img)
  img.save(png_path)

  production_date = str(datetime.now())
  png_files.append({
    'filename': png_path[4:],
    'north_bound': None,
    'east_bound': None,
    'south_bound': None,
    'west_bound': None,
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