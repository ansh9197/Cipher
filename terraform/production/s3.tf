data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "logs" {
  bucket = "${var.project}-logs-${data.aws_caller_identity.current.account_id}"
  tags   = { Name = "${var.project}-logs" }
}

resource "aws_s3_bucket" "models" {
  bucket = "${var.project}-models-${data.aws_caller_identity.current.account_id}"
  tags   = { Name = "${var.project}-models" }
}

resource "aws_s3_bucket_versioning" "logs" {
  bucket = aws_s3_bucket.logs.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_versioning" "models" {
  bucket = aws_s3_bucket.models.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_lifecycle_configuration" "logs" {
  bucket = aws_s3_bucket.logs.id
  rule {
    id     = "delete-old-logs"
    status = "Enabled"
    filter { prefix = "" }
    expiration { days = 90 }
  }
}
