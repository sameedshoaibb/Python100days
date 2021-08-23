def handler(event, context):    
    """
    This script finds & remove an old artifact / ami versions to avoid mess & over billing
    """
    import re
    import json
    import boto3
    from distutils.version import StrictVersion
    import time

    # Ec2 info
    EC2_REGION = "eu-central-1"

    # Connect EC2 boto3 resource
    EC2 = boto3.resource('ec2',
                         region_name=EC2_REGION)
    EC2_TEMPLATE = boto3.client('ec2',
                                region_name=EC2_REGION)
    # Get AMIs & Snamshots
    AMI = EC2.images.filter(
        Filters=[{'Name': 'tag:Team','Values': ['Backend','Devops']}],
        Owners=["self"]
    )

    def remove_snapshot():
        """
        This function removes all snapshots who's AMIs are no longer available / registerd
        """
        ami_id_list = [image.id for image in AMI]
        snapshots = EC2.snapshots.filter(
            Filters=[{'Name': 'tag:Team','Values': ['Backend','Devops']}],
            OwnerIds=["self"]
        )
        for snapshot in snapshots:
            resp = re.search(r"\bami-\w+", snapshot.description)
            if resp:
                if resp.group() not in ami_id_list:
                    snapshot.delete()

    def get_ami_id_of_running_instances():
        """
        This function get the ami id association with the running instances
        """
        instances = EC2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

        running_instances_ami_ids=[]
        for instance in instances:
            template_details = json.loads(json.dumps(EC2_TEMPLATE.get_launch_template_data(InstanceId=instance.id)))
            running_instances_ami_ids.append((EC2.Image(template_details['LaunchTemplateData']['ImageId'])))
        return(running_instances_ami_ids)

    def check_launch_template(running_instances_ami_ids,ami_id):
        """
        This function check the ami association with the launch template
        """
        for running_instances_ami_id in running_instances_ami_ids:
            if ( running_instances_ami_id == ami_id):
                return("true")
        return("false")

    def epoch_time():
        """
        This function generate the latest EPOCH time
        """
        local_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        time_format='%Y-%m-%d %H:%M:%S'
        epoch = int(time.mktime(time.strptime(local_time,time_format)))
        return(epoch)

    def insert(LAUNCH_TEMPLATE_ASSOCIATE_AMI,APP,ID,VERSION,EPOC,DATE):
        if APP not in  LAUNCH_TEMPLATE_ASSOCIATE_AMI:
            LAUNCH_TEMPLATE_ASSOCIATE_AMI[APP] = {}
            LAUNCH_TEMPLATE_ASSOCIATE_AMI[APP][ARTIFACT] = {}
            LAUNCH_TEMPLATE_ASSOCIATE_AMI[APP][ARTIFACT]["id"] = ID
            LAUNCH_TEMPLATE_ASSOCIATE_AMI[APP][ARTIFACT]["version"] = VERSION
            LAUNCH_TEMPLATE_ASSOCIATE_AMI[APP][ARTIFACT]["epoc"] = EPOC
            LAUNCH_TEMPLATE_ASSOCIATE_AMI[APP][ARTIFACT]["date"] = DATE

        else:
            LAUNCH_TEMPLATE_ASSOCIATE_AMI[APP][ARTIFACT] = {}
            LAUNCH_TEMPLATE_ASSOCIATE_AMI[APP][ARTIFACT]["id"] = ID
            LAUNCH_TEMPLATE_ASSOCIATE_AMI[APP][ARTIFACT]["version"] = VERSION
            LAUNCH_TEMPLATE_ASSOCIATE_AMI[APP][ARTIFACT]["epoc"] = EPOC
            LAUNCH_TEMPLATE_ASSOCIATE_AMI[APP][ARTIFACT]["date"] = DATE
        return()

    # Create artifactory of latest artifact only from same versions
    ARTIFACTORY = {}

    #Create Artifactory of old version AMI that still associate with launch template
    LAUNCH_TEMPLATE_ASSOCIATE_AMI = {}

    #Get running instances ami ids
    running_instances_ami_ids=get_ami_id_of_running_instances()

    #Get latest EPOCH time
    CURRENT_EPOCH = epoch_time()
    DIFFERENCE_IN_SECOND = 864000

    for image in AMI:
        DELETE_CHECK="false"
        ID = image.id
        ARTIFACT = '-'.join(image.name.split('-')[:-1])
        EPOC = image.name.split('-')[-1]
        DATE = image.creation_date.replace('T', ' ').strip('.000Z')

        if 'release' in ARTIFACT:
            APP = image.name.split('release')[0].rstrip('-')
            VERSION = 'release' + ARTIFACT.split('release')[1]
        elif 'hotfix' in ARTIFACT:
            APP = image.name.split('hotfix')[0].rstrip('-')
            VERSION = 'hotfix' + ARTIFACT.split('hotfix')[1]
        elif 'feature' in ARTIFACT:
            APP = image.name.split('feature')[0].rstrip('-')
            VERSION = 'feature' + ARTIFACT.split('feature')[1]
        elif 'epic' in ARTIFACT:
            APP = image.name.split('epic')[0].rstrip('-')
            VERSION = 'epic' + ARTIFACT.split('epic')[1]
        else:
            APP = '-'.join(image.name.split('-')[:-2])
            VERSION = image.name.replace('/', ' ').split('-')[-2]

        ami = EC2.Image(ID)    
        if (check_launch_template(running_instances_ami_ids,ami) == "false"):
            if ("hotfix" in ARTIFACT or "feature" in ARTIFACT or  "release" in ARTIFACT or "epic" in ARTIFACT):    
                if int(EPOC) not in range(CURRENT_EPOCH-DIFFERENCE_IN_SECOND, CURRENT_EPOCH):
                    DELETE_CHECK="true"
                    ami.deregister(DryRun=False)
                    #print(ARTIFACT, ID, DATE )

        if (APP not in ARTIFACTORY and "false" in DELETE_CHECK):
            ARTIFACTORY[APP] = {}
            ARTIFACTORY[APP][ARTIFACT] = {}
            ARTIFACTORY[APP][ARTIFACT]["id"] = ID
            ARTIFACTORY[APP][ARTIFACT]["version"] = VERSION
            ARTIFACTORY[APP][ARTIFACT]["epoc"] = EPOC
            ARTIFACTORY[APP][ARTIFACT]["date"] = DATE

        elif (APP in ARTIFACTORY and "false" in DELETE_CHECK):
            if ARTIFACT in ARTIFACTORY[APP]:
                if ARTIFACTORY[APP][ARTIFACT]["epoc"] < EPOC:
                    ami = EC2.Image(ARTIFACTORY[APP][ARTIFACT]['id'])

                    if (check_launch_template(running_instances_ami_ids,ami) == "false"):
                        ami.deregister(DryRun=False)
                        #print(ARTIFACT, ARTIFACTORY[APP][ARTIFACT]['id'], ARTIFACTORY[APP][ARTIFACT]['date'])
                        ARTIFACTORY[APP][ARTIFACT]["id"] = ID
                        ARTIFACTORY[APP][ARTIFACT]["epoc"] = EPOC
                        ARTIFACTORY[APP][ARTIFACT]["date"] = DATE
                    else:
                        LAUNCH_TEMPLATE_ASSOCIATE_AMI_ID = ARTIFACTORY[APP][ARTIFACT]["id"]
                        LAUNCH_TEMPLATE_ASSOCIATE_AMI_EPOC = ARTIFACTORY[APP][ARTIFACT]["epoc"]
                        LAUNCH_TEMPLATE_ASSOCIATE_AMI_DATE = ARTIFACTORY[APP][ARTIFACT]["date"]

                        #print(ARTIFACT, ARTIFACTORY[APP][ARTIFACT]['id'], ARTIFACTORY[APP][ARTIFACT]['date'])
                        ARTIFACTORY[APP][ARTIFACT]["id"] = ID
                        ARTIFACTORY[APP][ARTIFACT]["epoc"] = EPOC
                        ARTIFACTORY[APP][ARTIFACT]["date"] = DATE

                        insert(LAUNCH_TEMPLATE_ASSOCIATE_AMI,APP,LAUNCH_TEMPLATE_ASSOCIATE_AMI_ID,VERSION,LAUNCH_TEMPLATE_ASSOCIATE_AMI_EPOC,LAUNCH_TEMPLATE_ASSOCIATE_AMI_DATE)
                else:
                    ami = EC2.Image(ID)
                    if (check_launch_template(running_instances_ami_ids,ami) == "false"):
                        ami.deregister(DryRun=False)
                        #print(ARTIFACT, ID, DATE)
                    else:
                        insert(LAUNCH_TEMPLATE_ASSOCIATE_AMI,APP,ID,VERSION,EPOC,DATE)
            else:
                AVAILABLE_VERSIONS = []
                if ("hotfix" not in ARTIFACT and "feature" not in ARTIFACT and  "release" not in ARTIFACT and "epic" not in ARTIFACT and "base-prod" not in APP ):

                    for AVAILABLE_ARTIFACT in ARTIFACTORY[APP]:
                        if ("hotfix" not in AVAILABLE_ARTIFACT and  "feature" not in AVAILABLE_ARTIFACT and  "release" not in AVAILABLE_ARTIFACT and "epic" not in AVAILABLE_ARTIFACT ):
                            AVAILABLE_VERSIONS.append(ARTIFACTORY[APP][AVAILABLE_ARTIFACT]['version'].split('v')[-1])

                    VERSION_COUNT=len(AVAILABLE_VERSIONS)
                    if (VERSION_COUNT <= 1):
                        ARTIFACTORY[APP][ARTIFACT] = {}
                        ARTIFACTORY[APP][ARTIFACT]["id"] = ID
                        ARTIFACTORY[APP][ARTIFACT]["version"] = VERSION
                        ARTIFACTORY[APP][ARTIFACT]["epoc"] = EPOC
                        ARTIFACTORY[APP][ARTIFACT]["date"] = DATE

                    else:
                        AVAILABLE_VERSIONS.append(VERSION.split('v')[-1])
                        AVAILABLE_VERSIONS = sorted(AVAILABLE_VERSIONS, key=StrictVersion)   

                        if (AVAILABLE_VERSIONS[0] == VERSION.split('v')[-1]):
                            ami = EC2.Image(ID)
                            if (check_launch_template(running_instances_ami_ids,ami) == "false"):
                                ami.deregister(DryRun=False)
                                #print(ARTIFACT, ID, DATE)

                            else:
                                insert(LAUNCH_TEMPLATE_ASSOCIATE_AMI,APP,ID,VERSION,EPOC,DATE)
                        else:
                            ami = EC2.Image(ARTIFACTORY[APP][APP+"-v"+AVAILABLE_VERSIONS[0]]['id'])
                            if (check_launch_template(running_instances_ami_ids,ami) == "false"):
                                ami.deregister(DryRun=False)
                                del (ARTIFACTORY[APP][APP+"-v"+AVAILABLE_VERSIONS[0]])
                                ARTIFACTORY[APP][ARTIFACT] = {}
                                ARTIFACTORY[APP][ARTIFACT]["id"] = ID
                                ARTIFACTORY[APP][ARTIFACT]["version"] = VERSION
                                ARTIFACTORY[APP][ARTIFACT]["epoc"] = EPOC
                                ARTIFACTORY[APP][ARTIFACT]["date"] = DATE

                            else:
                                LAUNCH_TEMPLATE_ASSOCIATE_AMI_ID = ARTIFACTORY[APP][APP+"-v"+AVAILABLE_VERSIONS[0]]["id"]
                                LAUNCH_TEMPLATE_ASSOCIATE_AMI_VERSION = ARTIFACTORY[APP][APP+"-v"+AVAILABLE_VERSIONS[0]]["version"]
                                LAUNCH_TEMPLATE_ASSOCIATE_AMI_EPOC = ARTIFACTORY[APP][APP+"-v"+AVAILABLE_VERSIONS[0]]["epoc"]
                                LAUNCH_TEMPLATE_ASSOCIATE_AMI_DATE = ARTIFACTORY[APP][APP+"-v"+AVAILABLE_VERSIONS[0]]["date"]

                                del (ARTIFACTORY[APP][APP+"-v"+AVAILABLE_VERSIONS[0]])

                                ARTIFACTORY[APP][ARTIFACT] = {}
                                ARTIFACTORY[APP][ARTIFACT]["id"] = ID
                                ARTIFACTORY[APP][ARTIFACT]["version"] = VERSION
                                ARTIFACTORY[APP][ARTIFACT]["epoc"] = EPOC
                                ARTIFACTORY[APP][ARTIFACT]["date"] = DATE

                                insert(LAUNCH_TEMPLATE_ASSOCIATE_AMI,APP,LAUNCH_TEMPLATE_ASSOCIATE_AMI_ID,LAUNCH_TEMPLATE_ASSOCIATE_AMI_VERSION,LAUNCH_TEMPLATE_ASSOCIATE_AMI_EPOC,LAUNCH_TEMPLATE_ASSOCIATE_AMI_DATE)

                else:
                    ARTIFACTORY[APP][ARTIFACT] = {}
                    ARTIFACTORY[APP][ARTIFACT]["id"] = ID
                    ARTIFACTORY[APP][ARTIFACT]["version"] = VERSION
                    ARTIFACTORY[APP][ARTIFACT]["epoc"] = EPOC
                    ARTIFACTORY[APP][ARTIFACT]["date"] = DATE

    remove_snapshot()
    #print(json.dumps(ARTIFACTORY, indent=4))
    #print(json.dumps(LAUNCH_TEMPLATE_ASSOCIATE_AMI, indent=4))
    return {
        'statusCode': 200,
        'body': json.dumps('Function execution successful...!!')
    }
