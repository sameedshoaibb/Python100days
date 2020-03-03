#!/usr/bin/python
"""
This script calculate Apache MaxWorkers & Php-fpm MaxClient based on hardware specs & modify
httpd.conf & wwww.conf accordingly
"""

import multiprocessing
import subprocess

HTTPD_CONF = "/root/httpd.conf"
FPM_CONF = "/root/www.conf"

# Per process memory usage
HTTPD_PS_SIZE = 10
FPM_PS_SIZE = 20

# Get total cpu cores & memory
CORE = multiprocessing.cpu_count()
MEMORY = int(subprocess.check_output("free -m | grep Mem | awk {'print $2'}", shell=True))

# Calculate Max workers for apche & clients for php-fpm
MAX_WORKERS = (MEMORY * 0.9) // HTTPD_PS_SIZE
MAX_CLIENTS = (MEMORY * 0.9) // FPM_PS_SIZE

# Update httpd.conf
with open(HTTPD_CONF, 'r') as httpd_file:
    HTTPD_FILE = httpd_file.readlines()

with open(HTTPD_CONF, 'w') as httpd_file:
    for line in HTTPD_FILE:
        if 'ServerLimit' in line:
            httpd_file.write("    ServerLimit {}\n".format(MAX_WORKERS // 25))
        elif "StartServers" in line:
            httpd_file.write("    StartServers {}\n".format(CORE))
        elif "MaxRequestWorkers" in line:
            httpd_file.write("    MaxRequestWorkers {}\n".format(MAX_WORKERS))
        else:
            httpd_file.write(line)

# Update www.conf:

with open(FPM_CONF, 'r') as fpm_file:
    FPM_FILE = fpm_file.readlines()

with open(FPM_CONF, 'w') as fpm_file:
    for line in FPM_FILE:
        if 'pm.max_children' in line:
            fpm_file.write("pm.max_children = {}\n".format(MAX_CLIENTS))
        elif "pm.start_servers" in line:
            cal = CORE * 4
            fpm_file.write("pm.start_servers = {} \n".format(cal))
        elif "pm.min_spare_servers" in line:
            cal1 = CORE * 2
            fpm_file.write("pm.min_spare_servers {}\n".format(cal1))
        elif "pm.max_spare_servers" in line:
            cal2 = CORE * 4
            fpm_file.write("pm.max_spare_servers {}\n".format(cal2))
        else:
            fpm_file.write(line)

print("Apache Max Workers: %d"  %MAX_WORKERS)
print("Php-fpm Max Clients: %d" %MAX_CLIENTS)
