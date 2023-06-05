import boto3
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

                # Extract the folder name from the key
                folder_name = key.split('/')[0]

                # Check if the folder name (prefix) is older than 20220101
                if folder_name < '20220101':
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

                # Recursively call the function for each child prefix
                transition_to_glacier(bucket_name, child_prefix)



# Specify the bucket name and prefix
bucket_name = 'awss3terraformbucket'
prefix = 'class/' 

# Call the function to transition objects to Glacier Deep Archive
transition_to_glacier(bucket_name, prefix)




