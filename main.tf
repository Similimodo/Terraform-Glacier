module "transition" {
  source              = "./modules/s3_glacier_transition"
  bucket_name         = "your-bucket-name"
  transition_prefix   = "data/"
}

module "retrieval" {
  source         = "./modules/s3_glacier_retrieval"
  bucket_name    = "your-bucket-name"
  data_directory = "${path.module}/recreated_data"
}
