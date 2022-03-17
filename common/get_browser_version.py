import subprocess
from common.util import *

def get_version(browser_name):

    path_list = str(config.get('driver','version_path')).split(',')
    for i in range(len(path_list)):
        if str(browser_name).lower() in str(path_list[i]).lower():
            path=path_list[i]
            print('['+browser_name+'_version_path]:',path)
            break

    cmdArgs = ["wmic", "DATAFILE", "WHERE", r"NAME='{0}'".format(path), "GET", "Version", "/value"]
    process = subprocess.check_output(cmdArgs)
    print('['+browser_name+']', process.strip().decode())
    return process.strip().decode()

def get_browser_version(type):
    version_num=get_version(type)
    return version_num