'''
Created on Nov 30, 2016

@author: eason

Usage: Generate the positive sample description file used in haartraining.
'''
import sys
import glob
import argparse
import cv2

def get_args():
    """
    get arguments.
    """
    parser = argparse.ArgumentParser();
    parser.add_argument("-d",dest='sample_dir');
    parser.add_argument('-o',dest='descrip_file');
    args = parser.parse_args();
    return (args.sample_dir,args.descrip_file);

def get_file(dir_name,file_name):
    """
    get the goal description file.
    """
    # if path name ends with '/', remove the slash.
    if dir_name.endswith('/'):
        dir_name = dir_name[:-1];
    # get files in the directory.
    files = glob.glob('{0}/*.jpg'.format(dir_name));
    if files <= 0:
        sys.exit('Error. No <.jpg> file in the target directory.');
    # open description file.
    description_file = open(file_name,'w');
    buffer = [];
    for f in files:
        object_num = 1;
        start_x,start_y = 0,0;
        img = cv2.imread(f);
        width = img.shape[0];
        height = img.shape[1];
        info_buffer = [f, str(object_num), str(start_x), str(start_y), str(width), str(height)];
        info = ' '.join(info_buffer);
        info = info+'\n';
        buffer.append(info);
    description_file.writelines(buffer);
    description_file.close();
    
if __name__ == '__main__':
    sample_dir,descrip_file = get_args();
    if not sample_dir:
        sys.exit('Error. Need <-d sample_dir>.');
    if not descrip_file:
        sys.exit('Error. Need <-o descrip_file>');
    get_file(sample_dir,descrip_file);
