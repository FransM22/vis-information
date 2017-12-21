import json
import numpy
import os
from datetime import datetime
from pyhdf.SD import *
from PIL import Image
from RawDataPreparator import RawDataPreparator


class Preparator(RawDataPreparator):
  output_file_properties = None

  def __init__(self, paths):
    super().__init__(paths)
    self.__image_pairs = self.__get_image_pairs(self.input_paths())

  def write_output_files(self, output_dir_path):
    self.output_file_properties = []

    for path_1, path_2 in self.__image_pairs:
      filename = os.path.basename(path_1)
      output_filename = os.path.splitext(filename)[0] + '.png'
      output_path = os.path.join(output_dir_path, output_filename)

      image_identifier = filename.split('.')[1]
      img_1 = self.__process_image(path_1)
      img_2 = self.__process_image(path_2)

      combined_img = self.__combine_images(img_1, img_2)
      combined_img.save(output_path)

      http_access_path = os.path.relpath(output_path, 'www/')

      self.output_file_properties.append({
        'filename': http_access_path,
        'year': image_identifier,
        'production_datetime': str(datetime.now())
      })

  def write_output_root(self, output_file_path):
    if self.output_file_properties is None:
      print('Error. This method should only be called after output files have been written.')
    with open(output_file_path, 'w') as jsonfile:
      json.dump(self.output_file_properties, jsonfile)

  def __get_image_pairs(self, paths):
    all_paths = [x for x in sorted(paths)]
    pairs = []

    current_pair = []
    for path in all_paths:
      if len(current_pair) == 0:
        current_pair.append(path)
      elif len(current_pair) == 1:
        if current_pair[0].split('.')[1] == path.split('.')[1]:
          current_pair.append(path)
        else:
          print('Incomplete pair for ' + current_pair[0])
          current_pair = [path]
      if len(current_pair) == 2:
        pairs.append(current_pair)
        current_pair = []

    return pairs

  def __process_image(self, input_path):
    hdf_file = SD(input_path)

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

    data_matrix = numpy.array(hdf_obj.get())

    low, high = 12000, 15000  # This seems to be an appropriate range for all images

    # Uncomment the following lines to show the progress and some properties of each image
    # min_val = min(numpy.array(data_matrix).flatten())
    # max_val = max(numpy.array(data_matrix).flatten())
    # print('{} Min: {}, Max {}, Clipping to range ({}, {})'.format(os.path.basename(input_path), min_val, max_val, low, high))

    image_int_matrix = numpy.clip(data_matrix, low, high)
    image_int_matrix = numpy.divide(numpy.subtract(image_int_matrix, low), high - low)
    image_int_matrix *= 255

    img = Image.fromarray(numpy.uint8(image_int_matrix)).convert('RGBA')
    img = img.resize([img.size[0] // 2, img.size[1] // 2])  # Uses nearest neighbour by default

    # Set transparency
    col_img = []
    for val in img.getdata():
      intensity = val[0]
      opacity = 255
      if intensity == 0:
        opacity = 0
      col_img.append((intensity, 0, 0, opacity))
    img.putdata(col_img)
    return img

  def __combine_images(self, img_1, img_2):
    new_im = Image.new('RGBA', (img_1.size[0] + img_2.size[0], img_1.size[1]))
    new_im.paste(img_1, (0, 0))
    new_im.paste(img_2, (img_1.size[0], 0))

    return new_im