#!/usr/bin/python

'''
Made by sameed to check the traceroute issue
'''
from subprocess import check_output, CalledProcessError, STDOUT
import time
import datetime


command = ["traceroute", "iperf-fr-paris-01.pointtoserver.com"]
c1 = ["iperf3", "-c", "iperf-fr-paris-01.pointtoserver.com","-P 30"]

command3 = ["traceroute", "iperf-fr-paris-02.pointtoserver.com"]
c3 = ["iperf3", "-c", "iperf-fr-paris-02.pointtoserver.com","-P 30"]

command2 = ["traceroute", "iperf-us-newyork-01.pointtoserver.com"]
c2= ["iperf3","-c","iperf-us-newyork-01.pointtoserver.com","-P 30"]
for i in range(0,150):
    try:
        output = check_output(command, stderr=STDOUT).decode()
        output2 = check_output(command2, stderr=STDOUT).decode()
        output3 = check_output(command3, stderr=STDOUT).decode()
        o1 = check_output(c1, stderr=STDOUT).decode()
        o2 = check_output(c2, stderr=STDOUT).decode()
        o3 = check_output(c3, stderr=STDOUT).decode()

        with open("iperf-fr.txt","a") as f:
            now = datetime.datetime.now()
            f.write('\n' + "Current date and time : ")
            f.write(now.strftime("%Y-%m-%d %H:%M:%S"))
            f.write('\n'+ output)
            f.write('\n' + o1)
        with open("iperf-us.txt","a") as f:
            f.write('\n' + "Current date and time : ")
            f.write(now.strftime("%Y-%m-%d %H:%M:%S"))
            f.write('\n' + output2)
            f.write('\n' + o2)
        with open("iperf-fr-vultr.txt","a") as f:
            now = datetime.datetime.now()
            f.write('\n' + "Current date and time : ")
            f.write(now.strftime("%Y-%m-%d %H:%M:%S"))
            f.write('\n'+ output3)
            f.write('\n' + o3)
        success = True
        time.sleep(3600)
    except CalledProcessError as e:
        output = e.output.decode()
        success = False
