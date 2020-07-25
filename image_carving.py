#!/usr/bin/python3
# -*- coding:utf-8 -*-

# 2020.07.26 (Sun)
# Author : Jin Gunseung (comalmot)
# JPEG Carving Program in Directory. 
# Usage : python3 image_carving.py <src_folder> <dest_folder>

import os
import sys
import binascii

real_jpeg = []

def read_bin_data(path, filepath):
    f = open(path + filepath, 'rb')
    bin_data = f.read().hex()
    bin_data = binascii.unhexlify(bin_data)
    return bin_data

def check_sig(binary_data):

    if binary_data[:4] == b'\xff\xd8\xff\xe0' and binary_data[6:10] == b'JFIF' and binary_data[-2:] == b'\xff\xd9':
        print("==== [ JPEG/JFIF Format ] ====")

    elif binary_data[:4] == b'\xff\xd8\xff\xe1' and binary_data[6:10] == b'Exif' and binary_data[-2:] == b'\xff\xd9':
        print("==== [ JPEG/Exif Format - Digital Camera ] ====")
        print("==== [ Exchangeable Image File Format (EXIF) ] ====")

    elif binary_data[:4] == b'\xff\xd8\xff\xe8' and binary_data[6:11] == b'SPIFF' and binary_data[-2:] == b'\xff\xd9':
        print("==== [ Still Picture Interchange File Format (SOIFF) ] ====")
    
    else:
        print("This is not JPEG File.")
        print("Start Of Image or End Of Image is missing.")
        print("Please Check your file.")
        return

    return 1
    
def check_file(binary_data, filename):
    print("######## [File Name] : \"{}\" ########".format(filename))
    #print(binary_data[:2])
    #print(binary_data[-2:])
    #print(binary_data[6:10])
    result = check_sig(binary_data)
    
    if result:
        print("Signature Check Success!")
        return 1
    else:
        return 0

def return_jpeg_filelist(path):
    file_list = os.listdir(path)
    jpeg_file_list = [file for file in file_list if file.endswith(".jpeg")]
    return jpeg_file_list

if __name__=='__main__':
    if len(sys.argv) < 2:
        print("Usage : {} <source folder> <destination folder>".format(sys.argv[0]))
        exit(0)
    
    new_folder_path = './' + sys.argv[2]
    os.mkdir(new_folder_path)
    fl_ = return_jpeg_filelist(sys.argv[1])
    print(fl_)
    for tag in fl_:
        result = check_file(read_bin_data(sys.argv[1], tag), tag)
        if result:
            real_jpeg.append(tag)
            f = open(new_folder_path + tag, 'wb')
            f.write(read_bin_data(sys.argv[1], tag))
            f.close()
            print("{} is JPEG File.",format(tag))
            print("[+] Carving Success!")
        else:
            pass
