import csv
import json
from RawDataPreparator import RawDataPreparator


class Preparator(RawDataPreparator):
  def __init__(self, paths):
    super().__init__(paths)
    self.__observations = []

    for path in self.input_paths():
      self.__prepare_file(path)

  def write_output_files(self, output_dir_path):
    pass

  def write_output_root(self, output_file_path):
    with open(output_file_path, 'w') as jsonfile:
      json.dump(self.__observations, jsonfile)

  def __prepare_file(self, path):
    with open(path) as csvfile:
      csv_reader = csv.DictReader(csvfile)

      for row in csv_reader:
        observation = {
          'area': row['Area'],
          'year': row['Year'],
          'value': row['Value']
        }

        self.__observations.append(observation)