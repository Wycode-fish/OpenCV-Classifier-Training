#!/bin/bash

LOG="LOG: "
images_dir=""
vecs_dir=""
vec=""
num_img=0
negative_dir=""

# Get option arguments
if [ $# -le 1 ]
then 
	echo "Usage: ./createsamples.sh"
	echo "-f <images_dir>"
	echo "-v <vecs_dir>"
	echo "-n <number_of_image_use>"
	echo "-d <negative_images_dir>"
	echo "-o <vec>"
	exit 1
else
	while getopts "f:v:n:d:o:" opt
	do
		case ${opt} in
			f)
			images_dir=${OPTARG};;
			v)
			vecs_dir=${OPTARG};;
			o)
			vec=${OPTARG};;
			n)
			num_img=${OPTARG};;
			d)
			negative_dir=${OPTARG};;
			?)
			echo ${LOG}"can't recognize option parameter."
			exit 1;;
		esac
	done	
fi
echo -e ${LOG}"Get option arguments finished"

# Generate negative description file.
find ${negative_dir} -name '*.jpg' > negatives.dat
echo -e ${LOG}"Execution of generating negatives.dat finished" 

# Generate collection description file.
`python getdescrip.py -d $images_dir -o positives.dat`
echo -e ${LOG}"Execution of getdescrip.py finished"

# Create 10 samples from each image, store them in <vecs_dir>.
var_num=0
for FILE in $images_dir/*
do
	let "var_num=${var_num}+1"
	vec_name=${vecs_dir}/sample_${var_num}.vec
	echo "----test"
	opencv_createsamples -img ${FILE} -num 10 -bg negatives.dat -vec ${vec_name} -maxxangle 0.6 -maxyangle 0 -maxzangle 0.3 -maxidev 100 -bgcolor 0 -bgthresh 0 -w 20 -h 20
	echo "----"
	# test if reach specified image number.	
	if [ $var_num -eq $num_img ]
	then
		break
	fi
done
echo -e ${LOG}"Create samples from each image finished"

# Merge vecs.
`python mergevec.py -v ${vecs_dir} -o ${vec}`
echo -e ${LOG}"Execution of mergevec.py finished"

echo -e ${LOG}"createsamples.sh complete!"
