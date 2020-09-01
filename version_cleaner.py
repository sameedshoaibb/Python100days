#!/usr/bin/env python3
''' Pheli line'''

import boto3
REGION = 'eu-central-1'

def get_name():
    ''' Get data '''
    empty_list = []
    ec2 = boto3.resource('ec2', region_name=REGION)
    running_instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', \
                                                        'Values': ['running']}])
    for instance in running_instances:
        for tag in instance.tags:
            print("MR REHMAN",tag)
            if tag['Key'] == 'Name':
                name = tag['Value']
                empty_list.append(name)
    return empty_list

def data_simplify(sname):
    ''' Data modification '''
    shortlist_machines = []
    list_of_name = sname
    for i in list_of_name:
        if 'test' in i:
            shortlist_machines.append(i)
    return shortlist_machines

def version_split(data):
    ''' Version split '''
    unique = []
    for i in data:
        data = i.split('-v')
        sa =  data[0]+ " "+ "v"+ data[1]
        unique.append(sa)
    return unique

def unique(d):
    list_set = set(d) 
    unique_list = (list(list_set))
    for x in unique_list:
        print(x)

def main():
    ''' Main Fucntion '''
    name = get_name()
    data_simplify1 = data_simplify(name)
    d = version_split(data_simplify1)
    unique(d)

if __name__ == "__main__":
    main()
