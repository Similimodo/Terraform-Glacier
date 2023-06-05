import boto3
from datetime import datetime, timezone
from botocore.exceptions import ClientError
from multiprocessing import Pool

# Function to transition an object to Glacier Deep Archive
def transition_object_to_glacier(obj):
    bucket_name = obj['Bucket']
    key = obj['Key']
    last_modified = obj['LastModified'].replace(tzinfo=timezone.utc)
    cutoff_date = datetime(2023, 3, 31, tzinfo=timezone.utc)  # Set the cutoff date to 31st March 2023

    # Check if the object meets the transition criteria based on the last modified date
    if last_modified <= cutoff_date:
        try:
            # Transition the object to Glacier Deep Archive storage class
            s3_client = boto3.client('s3')
            s3_client.copy_object(
                Bucket=bucket_name,
                CopySource={'Bucket': bucket_name, 'Key': key},
                Key=key,
                StorageClass='DEEP_ARCHIVE'
            )
            print(f"Object '{key}' successfully transitioned to Glacier Deep Archive")
        except ClientError as e:
            print(f"Error transitioning object '{key}' to Glacier Deep Archive: {str(e)}")
    else:
        print(f"Object '{key}' doesn't meet the transition criteria, skipping.")

# Function to transition objects to Glacier Deep Archive using multiprocessing
def transition_to_glacier(bucket_name, prefix):
    s3_client = boto3.client('s3')

    # Create a paginator to retrieve objects in batches
    paginator = s3_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    # Create a multiprocessing pool with the desired number of processes
    pool = Pool(processes=4)  # Adjust the number of processes based on available resources

    # Iterate over the pages of objects
    for page in page_iterator:
        if 'Contents' in page:
            # Create a list of objects to transition
            objects_to_transition = []
            for obj in page['Contents']:
                objects_to_transition.append(obj)

            # Use multiprocessing to transition objects in parallel
            pool.map(transition_object_to_glacier, objects_to_transition)

        if 'CommonPrefixes' in page:
            # Iterate over child prefixes and transition objects within them
            for prefix_obj in page['CommonPrefixes']:
                child_prefix = prefix_obj['Prefix']
                transition_to_glacier(bucket_name, child_prefix)

    # Close the multiprocessing pool after processing all objects
    pool.close()
    pool.join()

# Specify the bucket name and prefix
bucket_name = 'awss3terraformbucket'
prefix = 'class/'

# Call the function to transition objects to Glacier Deep Archive
transition_to_glacier(bucket_name, prefix)
