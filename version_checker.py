#!/usr/bin/python3
''' This lambda function will identify the duplicate version's if it is up for 23 hours straight'''
from collections import defaultdict
import datetime
from packaging import version
import boto3
import json
import sys
import random
import requests

REGION = 'eu-central-1'
version_split = []
with_version = []
remove_images = []




ec2 = boto3.resource('ec2', region_name=REGION)
client = boto3.client('elbv2', region_name=REGION)
running_instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name','Values': ['running']}])

def lambda_handler(event, context):
    def get_unique_instance():
        ''' This function will get the instance, compare the version. If their are differnt version,
        this function will return the latest different version of the machine.
        if dialerrevamp-prod-api == dialerrevamp-prod-api, then match it's versions '''

        ec2info = defaultdict()
        for instance in running_instances:
            for tag in instance.tags:
                if 'Name'in tag['Key']:
                    name = tag['Value']
            ec2info[instance.id] = {
                'Name': name,   
                'Type': instance.instance_type,
                'State': instance.state['Name'],
                'Private IP': instance.private_ip_address,
                'Public IP': instance.public_ip_address,
                'Launch Time': instance.launch_time
                }
    
        for instance_id, instance in ec2info.items():
            instance_launch_time = instance["Launch Time"]
            name = instance["Name"]
            date_time = instance_launch_time.strftime("%Y-%m-%d %H:%M")
            #print("date_time",date_time)
            combined = name + " " + date_time
            with_version.append(combined)
            split = combined.split("-v")
            version_split.append(split)
    
        for loop_1 in range(len(version_split)):
            for loop_2 in range(len(version_split)):
                if version_split[loop_1][0] == version_split[loop_2][0]:
                    if version.parse(with_version[loop_1].split(" ")[0]) > \
                        version.parse(with_version[loop_2].split(" ")[0]):
                        remove_images.append(with_version[loop_1])
                        #remove_images.append(with_version[loop_2])
                    elif version.parse(with_version[loop_1].split(" ")[0]) < version.parse(with_version[loop_2].split(" ")[0]):
                        continue
                    else:
                        continue
    
                else:
                    continue
        
        unique_instance = list(set(remove_images))
        print("unique_instance",unique_instance)
        if not unique_instance:
            print("List is empty")
            return None
    
        add_time = []
        for instance in unique_instance:
            time1 = instance.split(" ")
            add_time.append(time1)
    
        return add_time


    def check_if(x): 
        get_listners = client.describe_load_balancers()
        arraysi = []
        for i in get_listners["LoadBalancers"]:
            listeners = client.describe_listeners(LoadBalancerArn= i["LoadBalancerArn"])
            for list in listeners["Listeners"]:
                for default in list["DefaultActions"]:
                    arraysi.append(default["TargetGroupArn"].split("/")[1])
    
        load_balancer = set(arraysi)
        route53=["cn-prod-api","bm-prod-cron","dr-prod-cron"]
        for inner in x:
            print("-----inner----",inner)
            for live_load_balancer in load_balancer:
                if inner[0] == live_load_balancer:
                    alert(live_load_balancer)
                elif inner[0][:15] in live_load_balancer:
                    alert(live_load_balancer)
                else:
                    print("Not matched inner[0]",live_load_balancer)
    
            for route in route53:
                print("ROUTE------X",route)
                if inner[0][:10] in route:
                    alert(inner[0])
                elif inner[0][:10] in route:
                    alert(inner[0])
                else:
                    print("nothing found",inner[0])
    
    def alert(machinename):
        url = ""
        title = (f"Duplicate Micorservices present :zap:")
        # message = ("{} is up from".format(machinename), in_minutes, "minutes")
        message = "{} | is Live".format(machinename)
        print("Message:",message)
        slack_data = {
            "username": "NotificationBot",
            "icon_emoji": ":satellite:",
            "channel" : "alerts",
            "attachments": [
                {
                    "color": "#9733EE",
                    "fields": [
                        {
                            "title": title,
                            "value": message,
                            "short": "false",
                        }
                    ]
                }
            ]
        }
        byte_length = str(sys.getsizeof(slack_data))
        headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
        response = requests.post(url, data=json.dumps(slack_data), headers=headers)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
    
    
    #     ''' Main Fucntion '''
    unique_instance = get_unique_instance()
    print("Main unique_instance",unique_instance)
    if not unique_instance:
        print("EXIT")
        exit()
    
    check_if(unique_instance)
