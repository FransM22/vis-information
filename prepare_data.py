#!/usr/bin/env python3

# prepare_data.py requires the following files:
# data/raw/total-final-energy-consumption.csv ( https://data.london.gov.uk/dataset/total-energy-consumption-borough )
# data/raw/hxxvxx_006_2015xxx.tif (these are preprocessed data files)

# prepare_data.py processes the raw data files and converts these to json
# files
import csv
import json
import os
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

print("\nDone")


# TODO - this is only a single sample file
tiffile = Image.open('data/raw/surface_temperature/h17v03_006_2015240204337.tif')
print('Converting data/raw/surface_temperature/h17v03_006_2015240204337.tif')
jpgfile = tiffile.convert('RGB')
jpgfile.save('www/data/h17v03_006_2015240204337.jpg', 'JPEG', quality=90)

with open('www/data/temperature_data.json', 'w') as jsonfile:
  json.dump({
    'filename': 'data/h17v03_006_2015240204337.jpg',
    'north_bound': 59.9958333333333,
    'south_bound': 50.0041666666667,
    'east_bound': -0.00649538000934793,
    'west_bound': -20.0083175793839,
    'production_datetime': '2015-08-28T20:43:37.000Z'
  }, jsonfile)

print("\nDone")