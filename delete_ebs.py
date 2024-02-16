#!/usr/bin/env python

#purpose: The script will look for disks in EBS that is not currently attached to any EC2 instance and delete them. 

import boto3

#aws security credentials
new_session = boto3.Session(aws_access_key_id="Access Key Here", aws_secret_access_key="Secret Key Here", region_name="Aws Region")

ec2 = new_session.resource('ec2')
volumes = ec2.volumes.all()

#counter variables
volume_count = 0
deleted_volumes = 0

#list of all discovered volumes
all_volumes = []

#list of volumes that has 0 attachments
volumes_to_delete = []

print("\nFetching volumes.... Please wait!\n")

for volume in volumes:
    volume_count+=1
    print("Volume Number:", volume_count)
    print("Volume ID:",volume.id)
    print("Volume Type:", volume.volume_type)
    print("Number of attachmets with the volume:",len(volume.attachments))
    print("--------------------------------------------")
    all_volumes.append(volume)

    if len(volume.attachments) == 0:
        volumes_to_delete.append(volume)

#terminate script if length is empty
if len(volumes_to_delete) == 0:
    print("No volumes found with 0 attachments. Terminating the script!")
    exit()

print("\nThese volumes are found with 0 attachments")

#list all volumes that would be deleted
#this block can be altered to write this information to a CSV file for auditing in a prod env
for volume in volumes_to_delete:
    print("(To be deleted) Volume ID:", volume.id)
    
choice = input("\nType yes to delete. NOTE: Only 'yes' will be accepted for deletion.\n")

if choice == "yes":
    print("\nDeletion in progress\n")
    for volume in volumes_to_delete:
        #this could be written to a txt file if needed in prod env to retain logs for audit
        print("Volume id {0} deleted".format({volume.id}))
        volume.delete()
        deleted_volumes+=1
    print("\n--------------------------------------------")
    print("{0} volumes discovered. {1} volumes deleted".format(volume_count, deleted_volumes))
else:
    exit()
