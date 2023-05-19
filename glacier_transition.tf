variable "bucket_name" {
  description = "The name of the S3 bucket"
}

variable "transition_prefix" {
  description = "The prefix to match the objects for transition"
}

resource "aws_s3_bucket_lifecycle_configuration" "lifecycle" {
  bucket = var.bucket_name

  rule {
    id     = "glacier-transition"
    status = "Enabled"

    transition {
      days          = 3
      storage_class = "GLACIER"
    }

    filter {
      prefix = var.transition_prefix
    }
  }
}
