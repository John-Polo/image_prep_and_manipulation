import os
import glob
import re

# Get a list with the full path. Change "directory, '*' + extension" to 
# "directory, '**', '*' + extension" to search recursively.
def list_files_with_glob(directory, extension):
    return glob.glob(os.path.join(directory, '*' + extension), recursive=False)

files_directory = 'Z:/Late_blight/ms3/lamp/bright'
ftype_pat = '*.jpg'
chiplist1 = list_files_with_glob(files_directory, ftype_pat)

files_directory = 'C:\\Users\\japolo\\Documents\\data\\LAMP\\'

datalampgr = list_files_with_glob(files_directory, ftype_pat)

# Tried to move the files that are green channel only to a new folder
greenf = [n for n in datalampgr if 'green' in n]
# OSError: can't move to a different disk drive for ...
#for i in range(0, len(greenf)):
#    os.rename(greenf[i], 'Z:\\Late_blight\\ms3\\lamp\\secondwave\\greenchannelonly\\' + greenf[i].split('\\')[-1])

def dir_to_list(directory, ftype_pat):
    """
    Returns a list of the date and time for the files in the given directory.
    """
    if not os.path.isdir(directory):
        raise ValueError(f"The directory {directory} does not exist or is not a directory.")
    if not os.access(directory, os.R_OK):
        raise ValueError(f"The directory {directory} is not readable.")
    if not ftype_pat:
        raise ValueError("File type pattern (ftype_pat) must be provided.")
    if not isinstance(ftype_pat, str):
        raise ValueError("File type pattern (ftype_pat) must be a string.")
    if not ftype_pat.startswith('*'):
        raise ValueError("File type pattern (ftype_pat) must start with '*' to match files.")
    temp_list = list_files_with_glob(directory, ftype_pat)
    print(len(temp_list))
    sublist = [re.findall(r'[0-9]{8}_[0-9]{6}', substring) for substring in temp_list]
    print(len(sublist))
    sublist = [x for xs in sublist for x in xs]
    print(len(sublist))
    return sublist

datalampfold = dir_to_list(files_directory, ftype_pat)

files_directory = 'Z:/Late_blight/ms3/lamp/lamp2022'

lamp22fold = dir_to_list(files_directory, ftype_pat)

brightfol = dir_to_list(files_directory, ftype_pat)

len(lamp22fold)
# 145
len(datalampfold)
# 423
len(brightfol)
# 277

allfiles = lamp22fold + datalampfold + brightfol
allfiles = list(set(allfiles))  # Remove duplicates

