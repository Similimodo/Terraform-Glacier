import boto3
from datetime import datetime, timezone
from botocore.exceptions import ClientError

def transition_to_glacier(bucket_name, prefix):
    s3_client = boto3.client('s3')

    # Create a paginator to retrieve objects in batches
    paginator = s3_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    # Iterate over the pages of objects
    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                last_modified = obj['LastModified'].replace(tzinfo=timezone.utc)
                cutoff_date = datetime(2023, 3, 31, tzinfo=timezone.utc)  # March 31st, 2023

                if last_modified <= cutoff_date:
                    try:
                        # Transition the object to Glacier Deep Archive storage class
                        s3_client.copy_object(
                            Bucket=bucket_name,
                            CopySource={'Bucket': bucket_name, 'Key': key},
                            Key=key,
                            StorageClass='DEEP_ARCHIVE'
                        )
                        print(f"Object '{key}' transitioned to Glacier Deep Archive")
                    except ClientError as e:
                        print(f"Error transitioning object '{key}' to Glacier Deep Archive: {str(e)}")
                else:
                    print(f"Object '{key}' doesn't meet transition criteria, skipping.")

        if 'CommonPrefixes' in page:
            for prefix_obj in page['CommonPrefixes']:
                child_prefix = prefix_obj['Prefix']
                transition_to_glacier(bucket_name, child_prefix)


# Specify the bucket name and prefix
bucket_name = 'samsung.s3.landing.stage'
prefix = 'IDL/'

# Call the function to transition objects to Glacier Deep Archive
transition_to_glacier(bucket_name, prefix)

