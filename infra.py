import pulumi
from pulumi_aws import s3

STACK_NAME = 'Staging'
REGION_NAME = 'us-east-1'
BUCKET_NAME = 'my-portfolio-bucket'

OUTPUT_KEY_BUCKET_NAME = 'bucket_name'

CONFIG_KEY_REGION = 'aws:region'
OUTPUT_KEY_REGION = 'region'

INDEX_DOCUMENT = 'index.html'
HTML_CONTENT = 'text/html'
HTML_ACL = 'public-read'


def create_bucket_and_object():
    bucket = s3.Bucket(
        BUCKET_NAME,
        website=s3.BucketWebsiteArgs(
            index_document=INDEX_DOCUMENT,
        )
    )
    bucket_object = s3.BucketObject(
        INDEX_DOCUMENT,
        acl=HTML_ACL,
        content_type=HTML_CONTENT,
        bucket=bucket.id,
        source=pulumi.FileAsset(INDEX_DOCUMENT)
    )
    pulumi.export(OUTPUT_KEY_BUCKET_NAME, bucket.bucket)
    pulumi.export(OUTPUT_KEY_REGION, bucket.region)
    return bucket, bucket_object
