output "ec2_public_ip" {
  value = aws_eip.cipher.public_ip
}

output "rds_endpoint" {
  value = aws_db_instance.postgres.endpoint
}

output "redis_endpoint" {
  value = aws_elasticache_cluster.redis.cache_nodes[0].address
}

output "ssh_command" {
  value = "ssh -i cipher-prod-key.pem ubuntu@${aws_eip.cipher.public_ip}"
}

output "ecr_registry" {
  value = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com"
}
