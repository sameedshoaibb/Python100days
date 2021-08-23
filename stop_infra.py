#!/usr/bin/python3
'''
This script will find the running resources and will stop it.
'''

import datetime
import boto3
REGION = "eu-central-1"
EC2 = boto3.resource('ec2', region_name=REGION)
RDS = boto3.client('rds', region_name=REGION)
NAME_OF_DB = [""]]
NAME_OF_DB_CLUSTER = [""]
NAME_OF_EC2 = ["old-infra"]
MATCHED_ID = []
AVAILABLE_DB = []
FIXED_TIME = 1
RESPONSE = RDS.describe_db_instances()
RESPONSE_CLUSTER = RDS.describe_db_clusters()

def lambda_handler(event, context):
    """ Main Fucntion """
    current_time = datetime.datetime.utcnow().strftime("%H:%M:%S")
    current_hour = datetime.datetime.utcnow().strftime("%H")
    print("UTC CURRENT TIME", current_time)
    print("Fixed_Time",FIXED_TIME)
    def start_infra():
        """ Starting the Function """
        print("Starting the Infra")
        for i in NAME_OF_EC2:
            stopped_instances = EC2.instances.filter(Filters=[{'Name': 'instance-state-name', \
                'Values': ['stopped']}, {'Name': 'tag:Application', 'Values': [i]}])

            for instance in stopped_instances:
                print("Starting the Instance :", instance.id)
                MATCHED_ID.append(instance.id)
        print("MAtched_ID_Start_Troubleshhoting",MATCHED_ID)
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
                
        # To start DB CLUSTER  
        status = RESPONSE_CLUSTER.get('DBClusters')[0].get('Status')
        NAME_OF_CLUSTER = RESPONSE_CLUSTER.get('DBClusters')[0].get('DBClusterIdentifier')
        if status == 'stopped':    
            resp = RDS.start_db_cluster(DBClusterIdentifier=NAME_OF_CLUSTER)
            print("STARTING THE DB CLUSTER")
            print('Requested to start cluster: ' + str(NAME_OF_CLUSTER))  
        else:
            print('RDS ' + str(NAME_OF_CLUSTER) + ' is ' + str(status))        

    def stop_infra():
        """ To stop the EC2 instance """
        print(int(current_hour))
        print("Stopping the infra")
        for i in NAME_OF_EC2:
            running_instances = EC2.instances.filter(Filters=[{'Name': 'instance-state-name', \
                'Values': ['running']}, {'Name': 'tag:Application', 'Values': [i]}])
            for instance in running_instances:
                print("Stopping the Instance :", instance.id)
                MATCHED_ID.append(instance.id)

        print("MAtched_ID_S_Troubleshhoting",MATCHED_ID)
        # EC2.instances.filter(InstanceIds=MATCHED_ID).stop()
        print(len(MATCHED_ID))
        if len(MATCHED_ID) != 0:
            print("Shutting down")
            print("MAtched_ID_Stop_Troubleshhoting",MATCHED_ID)
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
                
        """ To Stop the DB cluster """

        status = RESPONSE_CLUSTER.get('DBClusters')[0].get('Status')
        NAME_OF_CLUSTER = RESPONSE_CLUSTER.get('DBClusters')[0].get('DBClusterIdentifier')
        if status == 'available':    
            resp = RDS.stop_db_cluster(DBClusterIdentifier=NAME_OF_CLUSTER)
            print('Requested to stop rds: ' + str(NAME_OF_CLUSTER))  
        else:
            print('RDS ' + str(NAME_OF_CLUSTER) + ' is ' + str(status))
            
    if int(current_hour) == FIXED_TIME:
        start_infra()
    else:
        stop_infra()



