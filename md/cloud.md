# Feature: Cloud Misconfiguration Auditor

## Purpose
Reviews cloud configuration files (AWS, Azure, GCP) for security misconfigurations that could expose data or systems.

## Input
- Cloud config file content (AWS IAM JSON, S3 bucket policy, Azure/GCP config), pasted as text

## Output
A list of misconfigurations found, each with:
- What part of the config has the issue
- What the issue is
- Why it matters
- How to fix it

## Example Input
```json
{
  "Bucket": "company-data",
  "PublicAccessBlock": false,
  "Policy": {
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject"
  }
}
```

## Example Output
- Bucket "company-data" allows public access — PublicAccessBlock should be true
- Policy allows "*" (anyone) to GetObject — restrict Principal to specific accounts/roles

## What It Checks
- Public access to storage buckets
- Overly broad IAM permissions (wildcard actions/resources)
- Missing encryption settings
- Open security groups / firewall rules
- Unused or over-privileged roles