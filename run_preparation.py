#!/usr/bin/env python3
from vis_lib import PathRetriever
from vis_lib import EnergyConsumption
from vis_lib import Shapes
from vis_lib import Temperatures

# run_preparation.py requires the files as indicated by
#  vis_lib/PathRetriever.py
# The abstract methods in the vis_lib/RawDataPreparator.py RawDataPreparator
# class are implemented by the classes representing the data sets.

# run_preparation.py processes the raw data files and converts these to json
# and other data files usable by the server

print('Preparing shapes')
shape_paths = PathRetriever.Shapes()
shape_preparator = Shapes.Preparator(shape_paths)
shape_preparator.write_output()

print('\nPreparing energy consumption')
energy_consumption_paths = PathRetriever.EnergyConsumptions()
energy_preparator = EnergyConsumption.Preparator(energy_consumption_paths)
energy_preparator.write_output()

print('\nPreparing temperature files')
temperature_paths = PathRetriever.Temperatures()
temperature_preparator = Temperatures.Preparator(temperature_paths)
temperature_preparator.write_output()

print('\nDone')