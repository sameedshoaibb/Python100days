#!/usr/bin/python3
''' Service that will give running Testing machine's '''

import boto3

USER = [""]
ACTIVE_USERS = []
client = boto3.client('iam')

def lambda_handler(event, context):
    def list_of_users():
        ''' Getting the user's information '''

        response = client.list_users()
        paginator = client.get_paginator('list_access_keys')
        users_with_key = []
        for username in response['Users']:
            for response in paginator.paginate(UserName=username['UserName']):
                users_with_key.append(response["AccessKeyMetadata"])
        return users_with_key

    def simplify_active_users(data):
        ''' Formatting the active user's '''

        for i in data:
            for j in i:
                if j["Status"] == "Active":
                    ACTIVE_USERS.append(j)

        for i in USER:
            for j in ACTIVE_USERS:
                if i == j["UserName"]:
                    client.update_access_key(AccessKeyId=j["AccessKeyId"], \
                                            Status='Inactive', UserName=j["UserName"])
                    print("-- Deactivating {} Key --".format(i))
                    break
                # else:
                #     print("{} not found in the list".format(j["UserName"]))

    def main():
        ''' Main function '''
        active_users = list_of_users()
        simplify_active_users(active_users)


    main()
        
