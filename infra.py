from pulumi_aws import s3

# Create a simple test AWS bucket.

bucket = s3.Bucket(
    'my_portfolio_bucket',
)
