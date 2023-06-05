import boto3
from datetime import datetime

def transition_to_glacier(bucket_name, prefix=''):
    # Create an S3 client
    s3_client = boto3.client('s3')

    # Retrieve the list of objects in the bucket with the specified prefix
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    # Iterate over the objects
    for obj in response.get('Contents', []):
        # Get the key (object path) of the object
        key = obj['Key']

        # Check if the object meets the transition condition
        last_modified = obj['LastModified'].replace(tzinfo=None)
        transition_date = datetime(2023, 3, 31)
        if last_modified <= transition_date:
            # Transition the object to Glacier Deep Archive storage class and delete the original object
            s3_client.copy_object(
                Bucket=bucket_name,
                CopySource={'Bucket': bucket_name, 'Key': key},
                Key=key,
                StorageClass='DEEP_ARCHIVE',
                MetadataDirective='COPY',
                TaggingDirective='COPY',
                CopySourceIfModifiedSince=obj['LastModified'],
                Delete=True
            )
            print(f"Object '{key}' transitioned to Glacier Deep Archive.")
        else:
            print(f"Object '{key}' does not meet the transition condition.")

    # Get the list of common prefixes (subfolders)
    common_prefixes = response.get('CommonPrefixes', [])

    # Recursively transition objects in the child prefixes
    for prefix_obj in common_prefixes:
        child_prefix = prefix_obj['Prefix']
        transition_to_glacier(bucket_name, prefix=child_prefix)

# Specify the bucket name and prefix
bucket_name = 'cf-templates-vuh34z5z43s5-us-east-1'
prefix = 'hackerrank/'

# Call the function to transition objects to Glacier Deep Archive
transition_to_glacier(bucket_name, prefix)
