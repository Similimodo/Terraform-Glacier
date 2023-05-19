# terraform-Glacier
In this  code, we have two modules: s3_glacier_transition for transitioning the data folders in S3 to Glacier after three days, and s3_glacier_retrieval for recreating the directory structure during retrieval.

Ensure that you have the necessary folder structure with the module files in the appropriate locations. Adjust the bucket_name and transition_prefix variables in the main configuration to match your requirements.

When running terraform apply, the data folders in S3 with the prefix "data/" will be automatically transitioned to Glacier storage after three days. During retrieval, the s3_glacier_retrieval module will recreate the directory structure in the specified data_directory.