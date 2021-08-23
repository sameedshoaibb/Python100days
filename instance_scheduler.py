#!/usr/bin/python3
'''
If the resources are stopped, the script wil start it
                            &
If the resources are running, the script wil stop it.
'''

import datetime
import boto3
REGION = "us-east-2"
EC2 = boto3.resource('ec2', region_name=REGION)
RDS = boto3.client('rds', region_name=REGION)
NAME_OF_DB = [""]
NAME_OF_EC2 = [""]
MATCHED_ID = []
AVAILABLE_DB = []
FIXED_TIME = 5
RESPONSE = RDS.describe_db_instances()

def lambda_handler(event, context):
    """ Main Fucntion """

    current_time = datetime.datetime.utcnow().strftime("%H:%M:%S")
    current_hour = datetime.datetime.utcnow().strftime("%H")
    print("UTC CURRENT TIME", current_time)

    def start_infra():
        """ Starting the Function """

        print("Starting the Infra")
        for i in NAME_OF_EC2:
            stopped_instances = EC2.instances.filter(Filters=[{'Name': 'instance-state-name', \
                'Values': ['stopped']}, {'Name': 'tag:Application', 'Values': [i]}])

            for instance in stopped_instances:
                print("Starting the Instance :", instance.id)
                MATCHED_ID.append(instance.id)

        EC2.instances.filter(InstanceIds=MATCHED_ID).start()

        """ To Start the DB instance  """

        for i in RESPONSE['DBInstances']:
            if i['DBInstanceStatus'] == 'stopped':
                AVAILABLE_DB.append(i['DBInstanceIdentifier'])
            else:
                print("DB not N/A")

        for start_instance in AVAILABLE_DB:
            if start_instance in NAME_OF_DB:
                RDS.start_db_instance(DBInstanceIdentifier=start_instance)
                print("Starting the DB", start_instance)

    def stop_infra():
        """ To stop the EC2 instance """
        print("Stopping the infra")

        for i in NAME_OF_EC2:
            running_instances = EC2.instances.filter(Filters=[{'Name': 'instance-state-name', \
                'Values': ['running']}, {'Name': 'tag:Application', 'Values': [i]}])

            for instance in running_instances:
                print("Stopping the Instance :", instance.id)
                MATCHED_ID.append(instance.id)

        EC2.instances.filter(InstanceIds=MATCHED_ID).stop()

        """ To Stop the DB instance """

        for i in RESPONSE['DBInstances']:
            if i['DBInstanceStatus'] == 'available':
                AVAILABLE_DB.append(i['DBInstanceIdentifier'])
            else:
                print("DB not N/A")

        for stop_instance in AVAILABLE_DB:
            if stop_instance in NAME_OF_DB:
                RDS.stop_db_instance(DBInstanceIdentifier=stop_instance)
                print("Stopping the DB", stop_instance)

    if int(current_hour) == FIXED_TIME:
        start_infra()
    else:
        stop_infra()


