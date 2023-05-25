import boto3
from datetime import datetime

# Create an S3 client
s3_client = boto3.client('s3')

# Define the bucket name
bucket_name = 'awss3terraformbucket'

# Retrieve the list of objects in the bucket
response = s3_client.list_objects_v2(Bucket=bucket_name)

# Iterate over each object in the bucket
for obj in response['Contents']:
    # Get the key (file path) of the object
    obj_key = obj['Key']
    
    # Get the last modified date of the object
    last_modified = obj['LastModified']
    
    # Compare the last modified date with the cutoff date (March 31st, 2023)
    if last_modified.date() <= datetime(2023, 3, 31).date():
        # Copy the object to the same bucket with the desired storage class (Glacier Deep Archive)
        s3_client.copy_object(
            Bucket=bucket_name,
            CopySource={'Bucket': bucket_name, 'Key': obj_key},
            Key=obj_key,
            StorageClass='DEEP_ARCHIVE'
        )
        
        # Set the ACL (Access Control List) on the copied object to grant appropriate access
        s3_client.put_object_acl(
            Bucket=bucket_name,
            Key=obj_key,
            ACL='bucket-owner-full-control'
        )
