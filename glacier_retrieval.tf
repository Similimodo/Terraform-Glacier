variable "bucket_name" {
  description = "The name of the S3 bucket"
}

variable "data_directory" {
  description = "The directory to recreate the structure in"
}

data "aws_s3_bucket_objects" "retrieved_objects" {
  bucket = var.bucket_name
}

data "aws_s3_bucket_object" "retrieved_directories" {
  for_each = distinct([for obj in data.aws_s3_bucket_objects.retrieved_objects.objects : dirname(obj.key)])

  bucket = var.bucket_name
  key    = each.value
}

resource "null_resource" "recreate_structure" {
  for_each = data.aws_s3_bucket_object.retrieved_directories

  triggers = {
    directory = each.key
  }

  provisioner "local-exec" {
    command = "mkdir -p ${var.data_directory}/${each.key}"
  }
}
