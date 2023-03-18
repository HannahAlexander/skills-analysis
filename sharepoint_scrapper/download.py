from office365_api import SharePoint
from extract_text import extract_cv
import re
import sys, os
from pathlib import PurePath


def save_file(file_n, file_obj, FOLDER_DEST):
    file_dir_path = PurePath(FOLDER_DEST, file_n)
    with open(file_dir_path, 'wb') as f:
        f.write(file_obj)

def get_file(file_n, folder, FOLDER_DEST):
    file_obj = SharePoint().download_file(file_n, folder)
    save_file(file_n, file_obj, FOLDER_DEST)

def get_files(folder, FOLDER_DEST):
    files_list = SharePoint()._get_files_list(folder)
    for file in files_list:
        get_file(file.name, folder, FOLDER_DEST)

def get_files_by_pattern(keyword, folder, FOLDER_DEST):
    files_list = SharePoint()._get_files_list(folder)
    for file in files_list:
        if re.search(keyword, file.name):
            get_file(file.name, folder, FOLDER_DEST)
