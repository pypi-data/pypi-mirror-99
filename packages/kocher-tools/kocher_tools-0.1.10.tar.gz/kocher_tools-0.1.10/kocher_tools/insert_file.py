#!/usr/bin/env python
import os
import sys
import argparse
import json
import shutil
import logging

from Bio import SeqIO
from collections import defaultdict

from kocher_tools.config_file import ConfigDB
from kocher_tools.database import *
from kocher_tools.kocher_database import *

def uploadSampleParser ():
	'''
	Argument parser for adding samples

	Raises
	------
	IOError
		If the input, or other specified files do not exist
	'''

	def confirmFile ():
		'''Custom action to confirm file exists'''
		class customAction(argparse.Action):
			def __call__(self, parser, args, value, option_string=None):
				if not os.path.isfile(value):
					raise IOError('%s not found' % value)
				setattr(args, self.dest, value)
		return customAction

	def confirmFileList ():
		'''Custom action to confirm file exists in list'''
		class customAction(argparse.Action):
			def __call__(self, parser, args, values, option_string=None):
				# Loop the list
				for value in values:
					# Check if the file exists
					if not os.path.isfile(value):
						raise IOError('%s not found' % value)
				if not getattr(args, self.dest):
					setattr(args, self.dest, values)
				else:
					getattr(args, self.dest).extend(values)
		return customAction

	def metavarList (var_list):
		'''Create a formmated metavar list for the help output'''
		return '{' + ', '.join(var_list) + '}'

	upload_parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)

	# Input arguments
	schema_list = ('collection', 'storage', 'sequencing')
	upload_parser.add_argument('--schema', metavar = metavarList(schema_list), help = 'Schema (for upload)', choices = schema_list, required = True)

	input_method = upload_parser.add_mutually_exclusive_group(required = True)
	input_method.add_argument('--input-zip-file', help = 'Input ZIP Archive', type = str, action = confirmFile())
	input_method.add_argument('--input-file', help = 'Input file - for all schema except sequencing', type = str, action = confirmFile())
	input_method.add_argument('--sequencing-files', help = 'Sequencing input files', type = str, nargs = '+', action = confirmFileList())
	
	# Output arguments
	upload_parser.add_argument('--out-log', help = 'Filename of the log file', type = str, default = 'upload_samples.log')
	upload_parser.add_argument('--log-stdout', help = 'Direct logging to stdout', action = 'store_true')

	# Database arguments
	upload_parser.add_argument('--yaml', help = 'Database YAML config file', type = str, required = True, action = confirmFile())


	return upload_parser.parse_args()

def main():
			
	# Assign arguments
	upload_args = uploadSampleParser()

	'''
	# Check if log should be sent to stdout
	if upload_args.log_stdout:

		# Start logging to stdout for this run
		startLogger()

	else:

		# Start a log file for this run
		startLogger(log_filename = upload_args.out_log)

	# Log the arguments used
	logArgs(upload_args)
	'''

	# Create a list to store input file
	input_files = []

	# Check if a single input file has been specified
	if upload_args.input_file: input_files = [upload_args.input_file]

	# Check if sequencing files have been specified
	elif upload_args.sequencing_files: input_files = upload_args.sequencing_files

	# Check if a zip archive has been specified
	elif upload_args.input_zip_file:

		# Create a temporary directory
		zip_input_dir = tempfile.mkdtemp()

		# Extract zip archive into the temporary directory
		with zipfile.ZipFile(upload_args.input_zip_file, 'r') as zip_ref:
			zip_ref.extractall(zip_input_dir)

		# Assign the file(s) within the temporary directory
		for root, dirs, files in os.walk(zip_input_dir): 
			for file in files:
				input_files.append(os.path.join(root, file))


	# Check if a collection file has been specified
	if upload_args.schema == 'collection':

		# Check if there are too many files for the Collection schema
		if len(input_files) > 1: raise Exception (f'Type (collection) only supports a single input file')

		# Insert the file
		insertCollectionFileUsingConfig(upload_args.yaml, upload_args.schema, input_files[0])

	# Check if a storage file has been specified
	elif upload_args.schema == 'storage':

		# Check if there are too many files for the Storage schema
		if len(input_files) > 1: raise Exception (f'Type (storage) only supports a single input file')

		# Insert the file
		insertStorageFileUsingConfig(upload_args.yaml, input_files[0])

	# Check if a sequencing files have been specified
	elif upload_args.schema == 'sequencing':

		# Check if there are too many files for the Collection and Storage schema
		if len(input_files) not in [2, 3]: raise Exception (f'Type (sequencing) requires between two and three input files')

		# Insert the sequencing files
		insertBarcodeFilesUsingConfig(upload_args.yaml, upload_args.schema, input_files)

	# Delete the zip contents temp dir, if created
	if upload_args.input_zip_file: shutil.rmtree(zip_input_dir)

if __name__ == "__main__":
	main()