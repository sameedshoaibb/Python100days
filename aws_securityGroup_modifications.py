
#!/usr/bin/python3

import boto3
import subprocess
import time
import logging

#Create and configure logger 
logging.basicConfig(filename="/var/log/security_group.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 
#Creating an object 
logger=logging.getLogger() 
  
#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG)

for i in range(0,10):
    try:
        get_response = subprocess.check_output(["ping", "8.8.8.8","-c", "1"])
        get_IP = subprocess.check_output(["curl", "http://169.254.169.254/latest/meta-data/public-ipv4"])
        conn = boto3.client('ec2')
        conn.authorize_security_group_ingress(GroupId="sg-04df05f1130bdec85",IpProtocol="tcp",CidrIp=get_IP+"/32",FromPort=443,ToPort=443)
        sys.exit(0)
    except Exception as e:
        logger.error("Unable to Whitelist the IP")
        time.sleep(5)
