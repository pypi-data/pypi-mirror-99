import os
import logging
import string
import shutil
import gzip

from collections import OrderedDict
from Bio import SeqIO

from kocher_tools.fastq_multx import i5BarcodeJob, i7BarcodeJob
from kocher_tools.vsearch import *
from kocher_tools.compress import gzipCompress, gzipIsEmpty

class Multiplex (list):
	def __init__ (self, *arg, **kw):
		super(Multiplex, self).__init__(*arg, **kw)
		self.i5_file = ''
		self.i7_file = ''
		self.R1_file = ''
		self.R2_file = ''
		self.out_path = ''
		self.discard_empty_output = True

	def __contains__ (self, plate_str):
		if plate_str in [str(plate) for plate in self]:
			return True
		else:
			return False

	def __getitem__(self, plate_str):
		for plate in self:
			if str(plate) == plate_str:
				return plate

		raise Exception('%s not found in Multiplex' % plate_str) 

	@property
	def files (self):
		# Return files
		return [file for file in [self.i5_file, self.i7_file, self.R1_file, self.R2_file]]

	def assignOutputPath (self, out_path):

		# Assign the output path
		self.out_path = out_path

		# Create the directory, if needed
		if not os.path.exists(self.out_path):
			os.makedirs(self.out_path)

		logging.info('Output directory assigned: %s' % out_path)

	def assignFiles (self, i5_barcode_file, i7_barcode_file, r1_file, r2_file):
		self.i5_file = i5_barcode_file
		self.i7_file = i7_barcode_file
		self.R1_file = r1_file
		self.R2_file = r2_file

	def assignPlates (self, i5_map_filename):

		# Check if files have been assigned 
		if not self.files:
			
			# Raise an excpetion
			raise Exception('File assignment required for plate assignment')

		# Open the i5 map file
		with open(i5_map_filename) as i5_map_file:

			# Loop the i5 map file, line by line
			for i5_map_line in i5_map_file:

				# Split the line into: plate, barcode, locus
				i5_plate, i5_barcode, i5_locus = i5_map_line.split()

				# Assign the plate
				plate_object = Plate()

				# Assign the discard status
				plate_object.discard_empty_output = self.discard_empty_output

				# Assign the plate output path
				plate_object.out_path = self.out_path

				# Assign the plate name
				plate_object.name = i5_plate

				# Assign the locus
				plate_object.locus = i5_locus

				# Assign the filenames
				plate_object.assignFilenames()

				# Append the plate
				self.append(plate_object)

	def movePlates (self):

		# Loop the plates
		for plate in self:

			# Move the files
			plate.moveFiles()

	def deMultiplex (self, i5_map_filename):

		# Use the i5 map to demultiplex
		i5BarcodeJob(i5_map_filename, self.i5_file, self.i7_file, self.R1_file, self.R2_file, self.out_path, self.discard_empty_output)

	def compileMostAbundant (self, out_filename, out_format = 'fasta'):
		
		# Open the output file
		compiled_file = open(out_filename, 'w')

		# Loop each plate
		for plate in self:

			# Get the common fasta records from the plate
			for fasta_record in plate.yieldMostAbundant():

				# Write the 
				compiled_file.write(fasta_record.format(out_format)) 

		# Close the file
		compiled_file.close()

	def removeUnmatched (self):

		# Define an empty output path as default
		out_path = ''

		# Check if an output path has been defined
		if self.out_path:

			# Add a trailing directory symbol
			out_path = os.path.join(self.out_path, '')

		# Check if the empty output files were created
		if not self.discard_empty_output:

			# Remove the unmatched i5 output
			os.remove('%sunmatched_%s.fastq.gz' % (out_path, 'i5')) 

		# Remove the unmatched i7, R1, and R2 output
		os.remove('%sunmatched_%s.fastq.gz' % (out_path, 'i7')) 
		os.remove('%sunmatched_%s.fastq.gz' % (out_path, 'R1')) 
		os.remove('%sunmatched_%s.fastq.gz' % (out_path, 'R2'))

class Plate (list):
	def __init__ (self, *arg, **kw):
		super(Plate, self).__init__(*arg, **kw)
		self.name = ''
		self.locus = ''
		self.plate_i5_file = ''
		self.plate_i7_file = ''
		self.plate_R1_file = ''
		self.plate_R2_file = ''
		self.out_path = ''
		self.discard_empty_output = None

	def __str__(self):

		# Return the name of the plate
		return self.name

	def __contains__ (self, well_str):
		if well_str in [str(well) for well in self]:
			return True
		else:
			return False

	def __getitem__(self, well_str):
		for well in self:
			if str(well) == well_str:
				return well

		raise Exception('%s not found' % well_str) 

	@property
	def files (self):

		# Return the files, if assigned
		return [file for file in [self.plate_i5_file, self.plate_i7_file, self.plate_R1_file, self.plate_R2_file] if file]

	@property
	def well_path(self):

		# Assign the well path, using the out_path, name, and locus
		return os.path.join(self.out_path, self.name, self.locus)
	
	def assignFilenames (self):

		# Define an empty output path as default
		plate_out_path = ''

		# Check if an output path has been defined
		if self.out_path:

			# Add a trailing directory symbol
			plate_out_path = os.path.join(self.out_path, '')

		# Check if the empty output should be assigned
		if self.discard_empty_output == False:

			# Assign the i5 filename, by inserting the output path, plate name, and locus
			self.plate_i5_file = '%s%s_%s_i5.fastq.gz' % (plate_out_path, self.name, self.locus)

		# Assign the other filenames, by inserting the output path, plate name, and locus
		self.plate_i7_file = '%s%s_%s_i7.fastq.gz' % (plate_out_path, self.name, self.locus)
		self.plate_R1_file = '%s%s_%s_R1.fastq.gz' % (plate_out_path, self.name, self.locus)
		self.plate_R2_file = '%s%s_%s_R2.fastq.gz' % (plate_out_path, self.name, self.locus)

	def moveFiles (self):

		# Create the output path
		plate_out_path = os.path.join(self.out_path, self.name, self.locus)

		# Create the output directories
		if not os.path.exists(plate_out_path):
			os.makedirs(plate_out_path)

		# Check if the empty output should be moved
		if self.discard_empty_output == False:

			# Move the i5 file
			self.plate_i5_file = moveFile(self.plate_i5_file, plate_out_path)

		# Move/Rename the files
		self.plate_i7_file = moveFile(self.plate_i7_file, plate_out_path)
		self.plate_R1_file = moveFile(self.plate_R1_file, plate_out_path)
		self.plate_R2_file = moveFile(self.plate_R2_file, plate_out_path)

	def assignWells (self):

		# Check if files have been assigned 
		if not self.files:
			
			# Raise an excpetion
			raise Exception('File assignment required for well assignment')

		# Loop well letters, A to H
		for char in string.ascii_uppercase[:8]:

			# Loop well position, 1 to 12
			for pos in range(1, 13):

				# Save the well ID
				well_ID = char + str(pos)

				# Assign the Well
				well_object = Well()

				# Assing the discard status
				well_object.discard_empty_output = self.discard_empty_output

				# Assign the output path
				well_object.out_path = self.well_path

				# Save the ID
				well_object.ID = well_ID

				# Assign the plate the well is on
				well_object.on_plate = self.name

				# Assign the filenames
				well_object.assignFilenames()

				# Append the well
				self.append(well_object)

	def moveWells(self):

		# Loop the wells
		for well in self:

			# Move the files
			well.moveFiles()

	def deMultiplexPlate (self, i7_map_filename):

		# Use the i7 map to demultiplex
		i7BarcodeJob(i7_map_filename, self.plate_i7_file, self.plate_R1_file, self.plate_R2_file, self.well_path, self.discard_empty_output)

	def yieldMostAbundant (self):

		# Loop each well
		for well in self:

			# Get the common fasta records from the well
			for fasta_record in well.yieldMostAbundant():

				# Yield the the records from the well
				yield fasta_record

	def removeUnmatchedPlate (self):

		# Create the output path
		plate_out_path = os.path.join(self.out_path, self.name, self.locus, '')

		# Check if the empty output files were created
		if not self.discard_empty_output:

			# Remove the unmatched i5 output
			os.remove('%sunmatched_%s.fastq.gz' % (plate_out_path, 'i7')) 

		# Remove the unmatched R1 and R2 output
		os.remove('%sunmatched_%s.fastq.gz' % (plate_out_path, 'R1')) 
		os.remove('%sunmatched_%s.fastq.gz' % (plate_out_path, 'R2'))

class Well ():
	def __init__ (self):

		# General Args
		self.on_plate = ''
		self.ID = ''
		self.well_i7_file = ''
		self.well_R1_file = ''
		self.well_R2_file = ''
		self.out_path = ''
		self.well_dir = 'Demultiplexed'
		self.discard_empty_output = None

		# Merged Args
		self.merged_file = ''
		self.unmerged_R1_file = ''
		self.unmerged_R2_file = ''
		self.merged_dir = 'Merged'

		# Truncated Args
		self.truncated_file = ''
		self.truncated_dir = 'Truncated'

		# Filtered Args
		self.filtered_file = ''
		self.filtered_dir = 'Filtered'

		# Dereplicated Args
		self.dereplicated_file = ''
		self.dereplicated_dir = 'Dereplicated'

		# Clustered Args
		self.clustered_file = ''
		self.clustered_dir = 'Clustered'

		# Clustered Args
		self.common_file = ''
		self.common_dir = 'Common'

	def __str__(self):

		# Return the ID, if str() is used
		return self.ID

	@property
	def files (self):

		# Return the files, if they were defined
		return [file for file in [self.well_i7_file, self.well_R1_file, self.well_R2_file] if file]
	
	def assignFilenames (self):

		# Define an empty output path as default
		well_out_path = ''

		# Check if an output path has been defined
		if self.out_path:

			# Add a trailing directory symbol
			well_out_path = os.path.join(self.out_path, '')

		# Check if the empty output should be created
		if self.discard_empty_output == False:

			# Assign the i7 file
			self.well_i7_file = '%s%s_i7.fastq.gz' % (well_out_path, self.ID)

		# Assign the R1 and R2 filenames
		self.well_R1_file = '%s%s_R1.fastq.gz' % (well_out_path, self.ID)
		self.well_R2_file = '%s%s_R2.fastq.gz' % (well_out_path, self.ID)

	def moveFiles (self):

		# Create the output path
		well_out_path = os.path.join(self.out_path, self.well_dir)

		# Create the output directories
		if not os.path.exists(well_out_path):
			os.makedirs(well_out_path)

		# Check if the empty output should be moved
		if self.discard_empty_output == False:

			# Move the i7 file
			self.well_i7_file = moveFile(self.well_i7_file, well_out_path)

		# Move/Rename the R1 and R2 files
		self.well_R1_file = moveFile(self.well_R1_file, well_out_path)
		self.well_R2_file = moveFile(self.well_R2_file, well_out_path)

	def mergeWell (self):

		# Check if the R1 or R2 files are empty
		if gzipIsEmpty(self.well_R1_file) or gzipIsEmpty(self.well_R2_file):

			self.merged_file = ''
			self.unmerged_R1_file = ''
			self.unmerged_R2_file = ''

		else:

			# Add a trailing directory symbol to the output path
			merged_path = os.path.join(self.out_path, self.merged_dir, '')

			# Create the directory, if needed
			if not os.path.exists(merged_path):
				os.makedirs(merged_path)

			# Define the merged and unmerged files 
			self.merged_file = '%s%s_merged.fastq' % (merged_path, self.ID)
			self.unmerged_R1_file = '%s%s_notmerged_R1.fastq' % (merged_path, self.ID)
			self.unmerged_R2_file = '%s%s_notmerged_R2.fastq' % (merged_path, self.ID)

			# Merge the well R1 and R2 files
			mergePairs(self.ID, self.well_R1_file, self.well_R2_file, self.merged_file, self.unmerged_R1_file, self.unmerged_R2_file)

			# Gzip the files, return the updated filenames
			self.merged_file = gzipCompress(self.merged_file, return_filename = True)
			self.unmerged_R1_file = gzipCompress(self.unmerged_R1_file, return_filename = True)
			self.unmerged_R2_file = gzipCompress(self.unmerged_R2_file, return_filename = True)

	def truncateWell (self):

		# Check if the merged file is empty
		if self.merged_file == '' or gzipIsEmpty(self.merged_file):

			self.truncated_file = ''

		else:

			# Define the truncated path
			truncated_path = os.path.join(self.out_path, self.truncated_dir)

			# Create the directory, if needed
			if not os.path.exists(truncated_path):
				os.makedirs(truncated_path)

			# Define the truncated file
			self.truncated_file = os.path.join(truncated_path, '%s_stripped.fastq' % self.ID)

			# Truncate the merged file
			truncateFastq(self.merged_file, self.truncated_file)

			# Gzip the file, return the updated filename
			self.truncated_file = gzipCompress(self.truncated_file, return_filename = True)

	def filterWell (self):

		# Check if the truncated file is empty
		if self.truncated_file == '' or gzipIsEmpty(self.truncated_file):

			self.filtered_file = ''

		else:

			# Define the filtered path
			filtered_path = os.path.join(self.out_path, self.filtered_dir)

			# Create the directory, if needed
			if not os.path.exists(filtered_path):
				os.makedirs(filtered_path)

			# Define the filtered file
			self.filtered_file = os.path.join(filtered_path, '%s_filtered.fasta' % self.ID)

			# Filter the truncated file
			filterFastq(self.truncated_file, self.filtered_file)

			# Gzip the file, return the updated filename
			self.filtered_file = gzipCompress(self.filtered_file, return_filename = True)

	def dereplicateWell (self):

		# Check if the filtered file is empty
		if self.filtered_file == '' or gzipIsEmpty(self.filtered_file):

			self.dereplicated_file = ''

		else:

			# Define the dereplicated path
			dereplicated_path = os.path.join(self.out_path, self.dereplicated_dir)

			# Create the directory, if needed
			if not os.path.exists(dereplicated_path):
				os.makedirs(dereplicated_path)

			# Define the dereplicated file
			self.dereplicated_file = os.path.join(dereplicated_path, '%s_dereplicated.fasta' % self.ID)

			# Dereplicate the file
			dereplicateFasta(self.on_plate, self.ID, self.filtered_file, self.dereplicated_file)

			# Gzip the file, return the updated filename
			self.dereplicated_file = gzipCompress(self.dereplicated_file, return_filename = True)

	def clusterWell (self):

		# Check if the dereplicated file is empty
		if self.dereplicated_file == '' or gzipIsEmpty(self.dereplicated_file):

			self.clustered_file = ''

		else:

			# Define the clustered path
			clustered_path = os.path.join(self.out_path, self.clustered_dir)

			# Create the directory, if needed
			if not os.path.exists(clustered_path):
				os.makedirs(clustered_path)

			# Define the clustered file
			self.clustered_file = os.path.join(clustered_path, '%s_clustered.fasta' % self.ID) 

			# Cluster the file
			clusterFasta(self.on_plate, self.ID, self.dereplicated_file, self.clustered_file)

			# Gzip the file, return the updated filename
			self.clustered_file = gzipCompress(self.clustered_file, return_filename = True)

	def sortWell (self):

		# Define the sorted path
		sorted_path = os.path.join(self.out_path, self.clustered_dir)

		# Define the clustered file
		sort_file = os.path.join(sorted_path, '%s_sorted_clustered.fasta' % self.ID) 

		# Cluster the file
		sortFasta(self.on_plate, self.ID, self.clustered_file, sort_file)

		# Gzip the file, return the updated filename
		sort_file = gzipCompress(sort_file, return_filename = True)

		logging.info('%s-%s: Sorted clustered file' % (self.on_plate, self.ID))

		# Rename the clustered file
		self.clustered_file = sort_file

	def mostAbundantWell (self):

		# Check if the clustered file is empty
		if self.clustered_file == '' or gzipIsEmpty(self.clustered_file):

			self.common_file = ''

		else:

			# Define the common path
			common_path = os.path.join(self.out_path, self.common_dir)

			# Create the directory, if needed
			if not os.path.exists(common_path):
				os.makedirs(common_path)

			# Define the common file
			self.common_file = os.path.join(common_path, '%s_common.fasta.gz' % self.ID) 

			# Open file to store most common reads 
			common_file = gzip.open(self.common_file, 'wt')

			# Define an int to store the abundance of the read
			most_abundant_count = 0

			# Define an int to store the rank of the most abundance read
			most_abundant_rank = 0

			# Decompress the gzip file
			with gzip.open(self.clustered_file, "rt") as clustered_handle:

				# Loop the clustered file, line by line
				for clustered_line in clustered_handle:

					# Check if the line is a header
					if clustered_line.startswith('>'):

						# Get the abundance
						read_abundance = int(clustered_line.strip().split('=')[1])

						# Check if the abundance is higher than the stored value
						if read_abundance > most_abundant_count:

							# Update the count, and record is more abundant
							most_abundant_count = read_abundance

							# Get the rank
							read_rank = int(clustered_line.strip().split(';')[0].rsplit('_', 1)[1])

							# Update the rank
							most_abundant_rank = read_rank
			
			# Check if the read rank is not correctly ordered
			if most_abundant_rank != 1:

				# Sort the well to correct the order
				self.sortWell()

			# Decompress the gzip file
			with gzip.open(self.clustered_file, "rt") as clustered_handle:

				# Loop the clustered file, record by record
				for record in SeqIO.parse(clustered_handle, "fasta"):

					# Assign the abundance
					read_abundance = int(record.id.split('=')[1])

					# Check if the abundance is higher than the stored value
					if read_abundance >= (0.5 * most_abundant_count):

						# Write the fasta sequence to the common file
						common_file.write(record.format("fasta"))

			# Close the common file
			common_file.close()

	def yieldMostAbundant (self):

		# Confirm the file was specified
		if self.common_file:

			# Decompress the gzip file
			with gzip.open(self.common_file, "rt") as common_handle:

				# Loop the common file, record by record
				for record in SeqIO.parse(common_handle, "fasta"):

					# Yield the record as a fasta record
					yield record

def moveFile (file_to_move, out_path):

	# Assing the base filename of the file
	file_basename = os.path.basename(file_to_move)

	# Create the new filename
	new_file_filepath = os.path.join(out_path, file_basename)

	# Move the files
	shutil.move(file_to_move, new_file_filepath)

	# Update the filename
	return new_file_filepath
