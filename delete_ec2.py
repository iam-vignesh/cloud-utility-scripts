import boto3
import os

def check_aws_credentials():
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials is not None:
            print("Found credentials to access AWS!")
            return True
        else:
            print("Unbale to locate credentials for AWS!")
            return False
    except Exception as e:
        print("Script failed to load AWS credentials:", e)
        return False
    
check_aws_credentials()

# Initialize boto3 client
ec2_client = boto3.client('ec2')

# Retrieve information about all EC2 instances
response = ec2_client.describe_instances()

ec2_id = []

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        id = instance['InstanceId']
        ec2_id.append(id)

if len(ec2_id) == 0:
    print("No EC2 instances found. Exiting early!")
else:
    for id in ec2_id:
        delete_response = ec2_client.terminate_instances(InstanceIds=[id])
        status_code = str(delete_response['ResponseMetadata']['HTTPStatusCode'])
        status_code = status_code.strip()
        if status_code == '200':
            print("Status Code: {0} \nEC2 Instance with ID: {1} deleted!".format(status_code, id))
        else:
            print("Status Code: {0} \nUnexpected API response returned from AWS. Unable to confirm deletion. Please verify AWS console!".format(status_code))

