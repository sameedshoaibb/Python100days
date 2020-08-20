#!/usr/bin/python
"""
This script adds server's public ip into 'Server Accounting' RDS in California (us-west-1)
"""

import time
import logging
import subprocess
import boto3
from botocore.exceptions import ClientError

REGION = "us-west-1"
ACCESS_KEY_ID = "VAR_AWS_RDS_ACCESS_KEY_ID"
ACCESS_KEY_SECRET = "VAR_AWS_RDS_ACCESS_KEY_SECRET"

SECURITY_GROUP_NAME = "atom-dev"
PUBLIC_IP = (
    subprocess.check_output(["curl", "-s", "http://169.254.169.254/latest/meta-data/public-ipv4"]) \
    + "/32")

#Create and configure logger 
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(filename="/var/log/rds_access.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

# Connect RDS
RDS_CLIENT = boto3.client('rds',
    region_name=REGION,
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_KEY_SECRET
    )

# Check internet & add ip into db security group
for i in range(0,10):
    try:
        INTERNET_STATUS = subprocess.check_output(["ping", "8.8.8.8","-c", "1"])
        RDS_CLIENT.authorize_db_security_group_ingress(CIDRIP=PUBLIC_IP,
            DBSecurityGroupName=SECURITY_GROUP_NAME
            )
        break
    except ClientError as error:
        if error.response['Error']['Code'] == 'InvalidPermission.Duplicate':
            logger.error(error.response['Error']['Message'])
            break
        else:
            logger.error("No internet found on device")
            time.sleep(6)
