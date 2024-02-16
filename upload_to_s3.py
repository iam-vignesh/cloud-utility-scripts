import boto3
import argparse
import os

def check_aws_credentials():
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
    if access_key and secret_key:
        print("AWS credentials found in environment variables")
        return True
    else:
        print("AWS credentials not found in environment variables")
        return False

def upload_to_s3(bucket_name, file_path, object_name):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"File uploaded successfully to {bucket_name}/{object_name}")
    except FileNotFoundError:
        print(f"The file {file_path} was not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def check_pod_logs(podname, namespace):
    os.system("kubectl logs"+ podname+ "-n"+ namespace)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command line utility to fetch logs from EKS Cluster and upload files to S3")
    parser.add_argument("--bucket_name", help="Name of the S3 bucket")
    parser.add_argument("-u", "--upload", action="store_true", help="Upload file to S3 bucket")
    parser.add_argument("-f", "--file_path", help="Path to the file to upload")
    parser.add_argument("-name", "--object_name", help="Name to be given to the object in S3 for upload")
    parser.add_argument("-pl", "--podlogs", action="store_true", help="Find logs from container")
    parser.add_argument("-pn", "--podname", help="Find logs from container")
    parser.add_argument("-n", "--namespace", help="Find logs from container")
    args = parser.parse_args()

    if check_aws_credentials():
        if args.upload:
            if args.file_path and args.object_name:
                upload_to_s3(args.bucket_name, args.file_path, args.object_name)
            else:
                print("Please provide --file_path and --object_name for upload")
        elif args.podlogs:
            if args.podname and args.namespace:
                check_pod_logs(args.podname, args.namespace)
            else:
                print("Please provide pod name and namespace")
        else:
            print("Please specify either --upload or --podlogs")
    else:
        print("Please set AWS credentials in environment variables.")
