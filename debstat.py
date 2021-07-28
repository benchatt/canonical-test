#!/usr/bin/env python3
#second pass: still struggling with speed, but everything else is a little better
#to do: speed up?
#  get file from ftp location
import os,request,shutil,sys,tarfile

REPO = 'http://ftp.uk.debian.org/debian/dists/stable/main'

def pull_contents_gz(architecture: str) -> str:
    filename = f"Contents-{architecture}.gz"
    file_stream = request.get(f"{REPO}/{filename}",stream=True)
    if file_stream.ok:
        with open(filename,'wb') as fh:
            for chunk in file_stream.iter_content(chunk_size = 8 * 1024):
                # 8KB chunks was the example I saw of this, perhaps I should tinker with it
                if chunk:
                    fh.write(chunk)
                    fh.flush()
                    os.fsync(fh.fileno())
    else:
        print(f"Cannot download {REPO}/{filename}!")
        return None
    return filename

def extract_contents_index(gz_file: str) -> str:
    tar_fh = tarfile.open(gz_file)
    file_to_extract = tar_fh.getnames()[0]
    #assuming that the .gz file will always and only contain one file
    tar_fh.extractall()
    return file_to_extract

def get_top_ten(contents_index: str) -> list[tuple[str,int]]:
    top_ten = []
    with open(contents_index) as fh:
        for line in fh.readlines():
            preparsed_line = line.strip().split()
            if len(preparsed_line) != 2:
                continue
            (file,location) = preparsed_line
            if file.lower() == 'file' or location.lower() == 'location':
                continue
            #don't need this! Just count the commas and add one
            #location_list = location.split(',')
            #num_locations = len(location_list)
            num_locations = location.count(',')+1
            if len(top_ten) < 10:
                top_ten.append((file,num_locations))
                continue
            for i in range(len(top_ten)):
                if num_locations > top_ten[i][1]:
                    top_ten.insert(i,(file,num_locations))
                    break
            if len(top_ten) > 10:
                top_ten = top_ten[:10]
    return top_ten

def pretty_print_top_ten(top_ten: list[tuple[str,int]]):
    for i,entry in enumerate(top_ten):
        num_head = f"{i+1}."
        print(f"{num_head: >5}  {entry[0]: <35}{entry[1]}")

if __name__ == '__main__':
    top_ten = get_top_ten('/home/ben/Downloads/Contents-armhf')
    pretty_print_top_ten(top_ten)
