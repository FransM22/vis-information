from abc import ABC, abstractmethod


class RawDataPreparator(ABC):
  @abstractmethod
  def __init__(self, paths):
    self.__input_paths = paths.input_file_paths()
    self.__output_file_path = paths.output_file_path()
    self.__output_dir_path = paths.output_dir_path()

  @abstractmethod
  def write_output_files(self, output_dir_path):
    pass

  @abstractmethod
  def write_output_root(self, output_file_path):
    pass

  def write_output(self):
    self.write_output_files(self.output_dir_path())
    self.write_output_root(self.output_file_path())

  def input_paths(self):
    return self.__input_paths

  def output_file_path(self):
    return self.__output_file_path

  def output_dir_path(self):
    return self.__output_dir_path
