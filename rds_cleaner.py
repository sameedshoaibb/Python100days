''' Function to keep updated SG in OLD purevpn account'''
import json
import os
import boto3

EC2_REGION = "eu-central-1"

#  ACCESS_KEY_ID_OLD -> Old account which has RDS info
ACCESS_KEY_ID_OLD = os.environ['ACCESS_KEY_ID_OLD']
ACCESS_KEY_SECRET_OLD = os.environ['ACCESS_KEY_SECRET_OLD']
RDS_REGION = "us-west-1"

## ACCESS_KEY_ID_PURE -> new Account
ACCESS_KEY_ID_PURE = os.environ['ACCESS_KEY_ID_PURE']
ACCESS_KEY_SECRET_PURE = os.environ['ACCESS_KEY_SECRET_PURE']

# Connect RDS via boto3.client
RDS_CLIENT = boto3.client('rds',
                          region_name=RDS_REGION,
                          aws_access_key_id=ACCESS_KEY_ID_OLD,
                          aws_secret_access_key=ACCESS_KEY_SECRET_OLD)
SECURITY_GROUP_NAME = "gb-dev"

# AWS Account
FILTERS = [{'Name': "tag:Application", 'Values': ["Logs", "Test", \
              "Api"]}, {'Name': 'instance-state-name', 'Values': ['running']}]

EC2 = boto3.resource('ec2',
                     region_name=EC2_REGION)

FILTERS_PURE = [{'Name': "tag:Application", 'Values': ["Api"]}, \
                {'Name': 'instance-state-name', 'Values': ['running']}]

EC2_PURE = boto3.resource('ec2', region_name=EC2_REGION, aws_access_key_id=ACCESS_KEY_ID_PURE,
                          aws_secret_access_key=ACCESS_KEY_SECRET_PURE)

def handler(event, context):
    ''' Main Function '''
    instances = EC2.instances.filter(Filters=FILTERS)
    instances_ip = [instance.public_ip_address + "/32" for instance in instances]
    instances_pure = EC2_PURE.instances.filter(Filters=FILTERS_PURE)
    instances_ip_pure = [instance.public_ip_address + "/32" for instance in instances_pure]
    combine_list = [instances_ip.append(i) for i in instances_ip_pure]
    db_sg_data = RDS_CLIENT.describe_db_security_groups(DBSecurityGroupName=SECURITY_GROUP_NAME)
    authorized_ip = [ip['CIDRIP'] for ip in db_sg_data["DBSecurityGroups"][0]['IPRanges']]
    
    # Remove old ips which are not in use anymore
    for ip in authorized_ip:
        if ip == "5.5.5.5/32":
            pass
        elif ip not in instances_ip:
            RDS_CLIENT.revoke_db_security_group_ingress(CIDRIP=ip,
                                                        DBSecurityGroupName=SECURITY_GROUP_NAME)
            print(ip, "is revoked from ServerAccounting rds")

    # Authorize ips which are not already authorized
    for ip in instances_ip:
        if ip not in authorized_ip:
            RDS_CLIENT.authorize_db_security_group_ingress(CIDRIP=ip, \
                DBSecurityGroupName=SECURITY_GROUP_NAME)
            print(ip, "is authorized in ServerAccounting rds")



    print("Instances IPs: ", instances_ip)
    print("RDS SG IPs: ", authorized_ip)

    return {
        'statusCode': 200,
        'body': json.dumps('Function execution successful...!!')
    }

