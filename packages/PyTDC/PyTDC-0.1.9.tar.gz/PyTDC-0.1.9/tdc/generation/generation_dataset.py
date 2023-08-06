import pandas as pd
import numpy as np
import os, sys, json 
import warnings
warnings.filterwarnings("ignore")

from .. import base_dataset
from ..utils import *


class DataLoader(base_dataset.DataLoader):
	def __init__(self, name, path, print_stats, column_name):
		from ..utils import single_molecule_dataset_names 
		self.smiles_lst = distribution_dataset_load(name, path, single_molecule_dataset_names, column_name = column_name)  
		### including fuzzy-search 
		self.name = name 
		self.path = path 
		self.dataset_names = single_molecule_dataset_names
		if print_stats: 
			self.print_stats() 
		print_sys('Done!')
		
	def print_stats(self):
		print("There are " + str(len(self.smiles_lst)) + ' molecules ', flush = True, file = sys.stderr)

	def get_data(self, format = 'df'):
		if format == 'df':
			return pd.DataFrame({'smiles': self.smiles_lst})
		elif format == 'dict':
			return {'smiles': self.smiles_lst} 
		else:
			raise AttributeError("Please use the correct format input")

	def get_split(self, method = 'random', seed = 42, frac = [0.7, 0.1, 0.2]):
		'''
		Arguments:
			method: splitting schemes: random, cold_drug, cold_target
			seed: default 42
			frac: train/val/test split
		'''
		df = self.get_data(format = 'df')

		if method == 'random':
			return create_fold(df, seed, frac)
		else:
			raise AttributeError("Please use the correct split method")


class PairedDataLoader(base_dataset.DataLoader):
	def __init__(self, name, path, print_stats, input_name, output_name):
		'''
		Arguments:
			name: fuzzy name of the generation dataset. e.g., uspto50k, qed, drd, ... 
			path: directory path that stores the dataset, e.g., ./data
			print_stats: bool, whether print the stats.  
		returns:
			None
		'''
		from ..utils import paired_dataset_names 
		self.input_smiles_lst, self.output_smiles_lst = generation_paired_dataset_load(name, path, 
																					   paired_dataset_names, input_name, 
																					   output_name)  ### including fuzzy-search 
		self.name = name 
		self.path = path 
		self.dataset_names = paired_dataset_names
		if print_stats: 
			self.print_stats() 
		print_sys('Done!')
		
	def print_stats(self):
		print("There are " + str(len(self.input_smiles_lst)) + ' paired samples', flush = True, file = sys.stderr)


	def get_data(self, format = 'df'):
		if format == 'df':
			return pd.DataFrame({'input': self.input_smiles_lst, 'output':self.output_smiles_lst})
		elif format == 'dict':
			return {'input': self.input_smiles_lst, 'output':self.output_smiles_lst} 
		else:
			raise AttributeError("Please use the correct format input")


	def get_split(self, method = 'random', seed = 42, frac = [0.7, 0.1, 0.2]):
		'''
		Arguments:
			method: splitting schemes: random, cold_drug, cold_target
			seed: 42
			frac: train/val/test split
		'''

		df = self.get_data(format = 'df')

		if method == 'random':
			return create_fold(df, seed, frac)
		else:
			raise AttributeError("Please use the correct split method")

class DataLoader3D(base_dataset.DataLoader):
	### locally, unzip a folder, with the main file the dataframe with SMILES, Mol Object for various kinds of entities.
	### also, for each column, contains a sdf file. 

	def __init__(self, name, path, print_stats, dataset_names, column_name):
		self.df, self.path, self.name = three_dim_dataset_load(name, path, dataset_names)  
		if print_stats: 
			self.print_stats() 
		print_sys('Done!')
		
	def print_stats(self):
		print("There are " + str(len(self.df)) + ' data points ', flush = True, file = sys.stderr)

	def get_data(self, format = 'df', more_features = 'None'):
		
		if more_features in ['None', 'SMILES']:
			pass
		elif more_features in ['Graph3D', 'Coulumb', 'SELFIES']:
			try: 
				from rdkit.Chem.PandasTools import LoadSDF
				from rdkit import rdBase
				rdBase.DisableLog('rdApp.error')
			except:
				raise ImportError("Please install rdkit by 'conda install -c conda-forge rdkit'! ")	

			from ..chem_utils import MolConvert
			from ..metadata import sdf_file_names

			convert = MolConvert(src = 'SDF', dst = more_features)
			for i in sdf_file_names[self.name]:
				self.df[i + '_' + more_features] = convert(self.path + i + '.sdf')

		if format == 'df':
			return self.df
		else:
			raise AttributeError("Please use the correct format input")

	def get_split(self, method = 'random', seed = 42, frac = [0.7, 0.1, 0.2]):
		'''
		Arguments:
			method: splitting schemes: random, cold_drug, cold_target
			seed: default 42
			frac: train/val/test split
		'''
		df = self.get_data(format = 'df')

		if method == 'random':
			return create_fold(df, seed, frac)
		else:
			raise AttributeError("Please use the correct split method")


