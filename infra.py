import pulumi
from pulumi_aws import s3

BUCKET_NAME = 'my-portfolio-bucket'
OUTPUT_KEY_BUCKET_NAME = 'bucket_name'
OUTPUT_KEY_REGION = 'region'
INDEX_DOCUMENT = 'index.html'


def create_bucket():
    bucket = s3.Bucket(
        BUCKET_NAME,
        website=s3.BucketWebsiteArgs(
            index_document=INDEX_DOCUMENT,
        )
    )
    pulumi.export(OUTPUT_KEY_BUCKET_NAME, bucket.bucket)
    pulumi.export(OUTPUT_KEY_REGION, bucket.region)
    return bucket
