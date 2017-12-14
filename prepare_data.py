#!/usr/bin/env python3

# prepare_data.py requires the following files:
# data/raw/total-final-energy-consumption.csv ( https://data.london.gov.uk/dataset/total-energy-consumption-borough )

# prepare_data.py processes the raw data files and converts these to json
# files
import csv
import json
import os

if not os.path.exists('www/data/'):
  os.makedirs('www/data/')

with open('data/raw/total-final-energy-consumption.csv') as csvfile:
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