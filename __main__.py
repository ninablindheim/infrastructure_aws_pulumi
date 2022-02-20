import pulumi

import infra

pulumi.export('bucket_name', infra.bucket.id)
