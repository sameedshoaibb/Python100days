#!/usr/bin/env python3
''' Service that will give running Testing machine's '''

import boto3
REGION = 'eu-central-1'
ENV = "stage"

def get_name():
    ''' Get data '''
    empty_list = []
    ec2 = boto3.resource('ec2', region_name=REGION)
    running_instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', \
                                                        'Values': ['running']}])
    for instance in running_instances:
        for tag in instance.tags:
            # print("MR REHMAN",tag)
            if tag['Key'] == 'Name':
                name = tag['Value']
                empty_list.append(name)
    return empty_list

def data_simplify(sname):
    ''' Data modification '''
    shortlist_machines = []
    list_of_name = sname
    for i in list_of_name:
        if ENV in i:
            shortlist_machines.append(i)
    print(shortlist_machines)
    return shortlist_machines

def version_split(data):
    ''' Version split from service name '''
    unique = []
    for i in data:
        data = i.split('-v')
        service =  data[0]+ " "+ "v"+ data[1]
        unique.append(service)
    return unique

def unique(d):
    ''' Get only unique service '''
    list_set = set(d) 
    unique_list = (list(list_set))
    for x in unique_list:
        one = x.split(" ")
        if "iauth" in one[0]:
            print("platform-auth",one[1])
            
        elif "ivamproxy" in one[0]:
            print("vam-proxy",one[1])

        elif "gateway" in one[0]:
            print("platform-api-gateway",one[1])

        elif "vam" in one[0]:
            print("vam",one[1])

        elif "admin" in one[0]:
            print("platform-auth-admin",one[1])

        elif "ica" in one[0]:
            print("network-connection-logs",one[1])

        elif "queue-stage-api" in one[0]:
            print("platform-queue",one[1])
        
        elif "queue-stage-cron" in one[0]:
            print("platform-queue",one[1])

        elif "ib" in one[0]:
            print("platform-billing-api",one[1])

        elif "iwaf" in one[0]:
            print("platform-waf",one[1])

        elif "ianalytics" in one[0]:
            print("atom-bi-api",one[1])

        elif "rabbitmq" in one[0]:
            print("event-broadcast-manager",one[1])

        elif "test-cron" in one[0]:
            print("event-broadcast-cron",one[1])
            
        elif "billing" in one[0]:
            print("platform-billing",one[1])

        elif "ist" in one[0]:
            print("platform-speed-test",one[1])

        elif "idxn" in one[0]:
            print("dxn-api",one[1])

        elif "secure" in one[0]:
            print("secure-website",one[1])

        elif "ivap" in one[0]:
            print("vpn-account-profiling",one[1])
        else:
            print("Try again",one)

def main():
    ''' Main Fucntion '''
    name = get_name()
    shortlist_machines = data_simplify(name)
    splitted_version = version_split(shortlist_machines)
    unique(splitted_version)

if __name__ == "__main__":
    main()
