import os

class PathRetriever():
  def __init__(self):
    self.__paths = None
    self.__output_file_path = None
    self.__output_dir_path = None

  def from_path_description(self, directory, extension):
    self.__paths = list()
    self.__retrieve_and_select_paths(directory=directory, extension=extension)
    return self

  def from_list(self, paths):
    self.__paths = paths
    return self

  def input_file_paths(self):
    return self.__paths

  def output_file_path(self):
    return self.__output_file_path

  def output_dir_path(self):
    return self.__output_dir_path

  def set_output_file_path(self, output_file_path):
    self.__output_file_path = output_file_path

  def set_output_dir_path(self, output_dir_path):
    self.__output_dir_path = output_dir_path

  def __retrieve_and_select_paths(self, directory, extension):
    self.__paths.clear()

    for path in os.listdir(directory):
      if path[-len(extension):] == extension:
        self.__paths.append(directory + path)


def Shapes():
  pr = PathRetriever().from_path_description(
    directory='data/raw/shapes/',
    extension='geojson'
  )
  pr.set_output_file_path('www/data/shape_data.json')
  pr.set_output_dir_path('www/data/')

  return pr

def Temperatures():
  pr = PathRetriever().from_path_description(
    directory='data/raw/surface_temperature_v2/',
    extension='hdf'
  )
  pr.set_output_file_path('www/data/temperature_data.json')
  pr.set_output_dir_path('www/data/')

  return pr

def EnergyConsumptions():
  pr = PathRetriever().from_list(paths=['data/raw/total-final-energy-consumption.csv'])
  pr.set_output_file_path('www/data/energy_consumption.json')

  return pr