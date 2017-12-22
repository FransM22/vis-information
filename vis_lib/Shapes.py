import json
import os
import shutil
from .RawDataPreparator import RawDataPreparator


class Preparator(RawDataPreparator):
  output_file_paths = None

  def __init__(self, paths):
    super().__init__(paths)

  def write_output_files(self, output_dir_path):
    self.output_file_paths = []

    for input_path in self.input_paths():
      filename = os.path.basename(input_path)
      output_path = os.path.join(output_dir_path, filename)
      shutil.copyfile(input_path, output_path)

      http_access_path = os.path.relpath(output_path, 'www/')
      self.output_file_paths.append(http_access_path)

  def write_output_root(self, output_file_path):
    if self.output_file_paths is None:
      print('Error. This method should only be called after output files have been written.')
    with open(output_file_path, 'w') as jsonfile:
      json.dump(self.output_file_paths, jsonfile)
