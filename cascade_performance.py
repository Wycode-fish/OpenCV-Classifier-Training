import sys
import cv2
import glob
import argparse

def get_args():
	"""
	get arguments	
	"""
	parser=argparse.ArgumentParser();
	parser.add_argument("-d",dest="dir_name");
	parser.add_argument("-x",dest="xml_name");
	parser.add_argument("-ni",dest="rec_flag");
	args=parser.parse_args();
	return [args.dir_name,args.xml_name,args.rec_flag];

def process(dir_name,xml_name,rec_flag):
	"""
	process test images
	"""
	# check if directory name ends with '/'
	if dir_name.endswith("/"):
		dir_name=dir_name[:-1];
	# generate classifier from .xml
	clf = cv2.CascadeClassifier(xml_name);
	# process test images
	files=glob.glob(dir_name+'/*.jpg');
	info_dict = {};
	for f in files:
		img = cv2.imread(f);
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY);
		objs = clf.detectMultiScale(
			gray,
			minNeighbors=4,
			scaleFactor=1.1,
			minSize=(20,20),
			flags=cv2.CASCADE_SCALE_IMAGE
		);
		
		positions = get_position(f);
		false_positives = 0;
		hit = 0;
		miss = 0;
		# get target coordinate
		if len(objs) == 0:
			false_positives = 0;
			hit = 0;
			miss = 1;
		elif len(objs) != 0:
			for (x,y,w,h) in objs:
				# highlight the object by rectangles.
				cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2);

				if x<=positions[1]+positions[3]*0.5 and y<=positions[2]+positions[4]*0.5 and x+w>=positions[1]+positions[3]-positions[3]*0.5 and y+h>=positions[2]+positions[4]-positions[4]*0.5:
					hit = 1;
				else:
					false_positives = false_positives + 1;			
			if hit != 1:
				miss = 1;
		# if -ni is 'yes', save the retangled images with postfix "_det"
		if rec_flag == 'yes':
			cv2.imwrite(f.split(".")[0].split("/")[0]+"/det_"+f.split(".")[0].split("/")[-1]+"."+f.split(".")[1],img);
		info_dict[f.split("/")[-1]] = [hit,false_positives,miss];
	# print out the whole result.
	print_result(info_dict);

def get_position(fname):
	"""
	read the target's position from the image file name.
	"""
	positions = fname.split("/")[-1].split(".")[0].split("_");
	result = [];
	for pos in positions:
			result.append(int(pos));
	return result;

def print_result(info_dict):
	"""
	print the form shows the result.
	"""
	print "info_dict length: "+str(len(info_dict.keys()));
	print "|------------------------------------|-------|-------|-------|";
	print "|                image               |  hit  |  F_A  |  MIS  |";
	print "|------------------------------------|-------|-------|-------|";
	
	hit_num = 0;
	fa_num = 0;
	miss_num = 0;
	for key in info_dict.keys():
		print "|"+key.center(36)+"|"+str(info_dict[key][0]).center(7)+"|"+str(info_dict[key][1]).center(7)+"|"+str(info_dict[key][2]).center(7)+"|";
		print "|------------------------------------|-------|-------|-------|";
		hit_num = hit_num + info_dict[key][0];
		fa_num = fa_num + info_dict[key][1];
		miss_num = miss_num + info_dict[key][2];
	
	#print "|"+"total".center(36)+"|"+str(round(float(hit_num)/float(len(key)),2)).center(7)+"|"+str(fa_num).center(7)+"|"+str(miss_num).center(7)+"|";
	print "|"+"total".center(36)+"|"+str(hit_num).center(7)+"|"+str(fa_num).center(7)+"|"+str(miss_num).center(7)+"|";
	print "|------------------------------------|-------|-------|-------|";
	print "*** *** *** ***"
	hit_rate = float(hit_num) / float(len(info_dict.keys()));
	print "hit rate: "+str(hit_rate);

if __name__ == "__main__":
	dir_name, xml_name, rec_flag = get_args();
	if not dir_name or not xml_name or not rec_flag:
		print "- Usage: ";
		print "./cascade_performance.sh <-d> <-x> <-ni>"
		sys.exit("- end");
	process(dir_name, xml_name, rec_flag);
