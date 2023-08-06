#!/usr/bin/env python
import os
import sys
import csv
import argparse
import pandas as pd
from collections import defaultdict
from kocher_tools.gff import *

def gffArgs ():

	'''
	Argument parser

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

	gff_parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)

	# Assign I/O arguments
	gff_parser.add_argument('--gff-file', help = "Defines the GFF filename", type = str, action = confirmFile(), required = True)
	gff_parser.add_argument('--chrom-size-file', help = "Defines the chromosome size filename (as tsv)", type = str, action = confirmFile(), required = True)
	gff_parser.add_argument('--position-file', help = "Defines the position filename (as tsv)", type = str, action = confirmFile(), required = True)
	gff_parser.add_argument('--out-file', help = "Defines the output filename (as tsv). Defaults to out.tsv", type = str, default = 'out.tsv')

	# Assign the bp values for added features
	gff_parser.add_argument('--promoter-bp', help = "Defines the promoter length", type = int, default = 5000)
	gff_parser.add_argument('--upstream-bp', help = "Defines the upstream length", type = int, default = 10000)
	gff_parser.add_argument('--downstream-bp', help = "Defines the downstream length", type = int, default = 10000)

	'''
	Assign features arguments. Some features appear multiple times due to alternative 
	feature names - i.e. ['five_prime_UTR', 'five_utr']. This will not cause an error
	as features not found within the file will be ignored.
	'''
	feature_set = ['tss_upstream', 'tss_flanks', 'five_prime_UTR', 'five_utr', 'exon', 'CDS', 'first_intron', 'intron', 'three_prime_UTR', 'three_utr', 'intergenic']
	gff_parser.add_argument('--feature-set', help = "Defines the feature set. Feature not it list will be ignored", type = str, nargs = '+', default = feature_set)
	priority_list = ['promoter', 'upstream', 'downstream', 'five_prime_UTR', 'five_utr', 'exon', 'CDS', 'first_intron', 'intron', 'three_prime_UTR', 'three_utr', 'intergenic']
	gff_parser.add_argument('--priority-order', help = "Defines the priority of features", type = str, nargs = '+', default = priority_list)

	# Return arguments
	return gff_parser.parse_args()

# Assign the arguments using argparse
gff_args = gffArgs()

# Assign a set with all the possible features
feature_set = gff_args.feature_set + ['upstream', 'promoter', 'downstream']

# Check if features in the priority are not in the feature set
unique_priority_features = list(set(gff_args.priority_order) - set(feature_set))
if unique_priority_features: raise Exception(f'Feature(s) found in --priority-order not in --feature-set: %s' % ', '.join(unique_priority_features))

# Create the database
gff_db = createDatabase(gff_args.gff_file)

'''
Read in the chromosome sizes file and confirm the sizes are ints
then read in the chromosome positions file and group the positions
'''
chrom_sizes = pd.read_csv(gff_args.chrom_size_file, sep = '\t', header = None, usecols=[0, 1], dtype = {0: str, 1: int})
chrom_positions = pd.read_csv(gff_args.position_file, sep = '\t', header = None, usecols=[0, 1], dtype = {0: str, 1: int})
grouped_chrom_positions = {_cnname:_cpos[1].values for _cnname, _cpos in chrom_positions.groupby(by=[0])}

try:	
	# Create the output file, and write the header
	output_file = open(gff_args.out_file, 'w')
	output_file.write('#%s\n' % ' '.join(sys.argv))
	headers = ['Chromosome', 'Position', 'All Features', 'All Features Genes', 'Features w/ Priority', 'Features w/ Priority Genes']
	output_writer = csv.DictWriter(output_file, fieldnames = headers, delimiter = '\t')
	output_writer.writeheader()

	'''
	Loop the GFF database by each chromosome and then calculate the stats
	for each position, first w/priority and then with no priority
	'''
	for chrom_name, chrom_size in chrom_sizes.values:
		if chrom_name not in grouped_chrom_positions: continue
		feature_dict_w_priority  = posCounts(gff_db, chrom_name, chrom_size, grouped_chrom_positions[chrom_name], prioritize = True, **vars(gff_args))
		feature_dict_no_priority = posCounts(gff_db, chrom_name, chrom_size, grouped_chrom_positions[chrom_name], **vars(gff_args))

		## Add the features to the feature list
		for position in feature_dict_w_priority.keys():
			if position not in feature_dict_w_priority: raise Exception('Unable to merge position data')

			output_writer.writerow({'Chromosome':chrom_name, 
									'Position':position, 
									'All Features':', '.join([_fd[0] for _fd in feature_dict_no_priority[position]]),
									'All Features Genes':', '.join([_fd[1] for _fd in feature_dict_no_priority[position]]),
									'Features w/ Priority':', '.join([_fd[0] for _fd in feature_dict_w_priority[position]]),
									'Features w/ Priority Genes':', '.join([_fd[1] for _fd in feature_dict_w_priority[position]])})
	
	# Close the output file
	output_file.close()

except:
	output_file.close()
	os.remove(gff_args.out_file)
	raise
