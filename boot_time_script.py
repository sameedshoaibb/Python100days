#!/usr/bin python

import multiprocessing
import subprocess

HTTPD_PATH = "/home/sameed-shoaib/Documents/Atom/Master_Folder/Terraform/httpd.conf"
PHP_conf = "/home/sameed-shoaib/Documents/Atom/Master_Folder/Terraform/php.conf"

PHP_FPM_SIZE = 20
HTTPD_SIZE = 10

#To get no of cores
CORE = multiprocessing.cpu_count()

#To get memory 
MEMORY = subprocess.check_output("free -m | grep Mem | awk {'print $2'}", shell=True)
MAX_WORKERS = (int(MEMORY) - 256) / HTTPD_SIZE
MAX_CLIENTS = (int(MEMORY) - 256) / PHP_FPM_SIZE

with open(HTTPD_PATH, 'r') as f:
    lines = f.readlines()

with open(HTTPD_PATH, 'w') as g:
    for line in lines:
        if 'ServerLimit' in line:
            g.write("\tServerLimit " + str(MAX_WORKERS))
        elif "StartServers" in line:
            g.write("\n\tStartServers {}\n".format(CORE))
        elif "MaxRequestWorkers" in line:
            g.write("\tMaxRequestWorkers {}\n".format(MAX_WORKERS))     
        else:
            g.write(line)


with open(PHP_conf, 'r') as f:
    lines = f.readlines()

with open(PHP_conf, 'w') as g:
    for line in lines:
        if 'pm.max_children' in line:
            g.write("\tpm.max_children = {}\n".format(MAX_CLIENTS))
        elif "pm.start_servers" in line:
            cal = CORE * 4
            g.write("\tpm.start_servers = {} \n".format(cal))
        elif "pm.min_spare_servers" in line:
            cal1 = CORE * 2
            g.write("\tpm.min_spare_servers {}\n".format(cal1))   
        elif "pm.max_spare_servers" in line:
            cal2 = CORE * 4
            g.write("\tpm.max_spare_servers {}\n".format(cal2))   
        else:
            g.write(line)



    
