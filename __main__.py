"""An AWS Python Pulumi program"""

from pulumi_aws import s3

import pulumi

# Create an AWS resource (S3 Bucket)
# Set website property on bucket to make it able to serve the index.html File
# as a static website.
bucket = s3.Bucket('my-bucket',
                   # website=s3.BucketWebsiteArgs(
                   #     index_document="index.html",
                   )

# # FileAsset class will assign the content of the file to a new BucketOject
# bucketObject = s3.BucketObject(
#     'index.html',
#     # public-read so that it can be accessed anonymously over the Internet
#     acl='public-read',
#     # content type so that it is served as HTML
#     content_type='text/html',
#     bucket=bucket.id,
#     source=pulumi.FileAsset('index.html')
# )

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
# # export the resulting bucket's endpoint URL so you can easily access it
# pulumi.export('bucket_endpoint', pulumi.Output.concat('http://', bucket.website_endpoint))
