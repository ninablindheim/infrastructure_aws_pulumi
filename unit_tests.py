import unittest

import pulumi


class MyMocks(pulumi.runtime.Mocks):
    def new_resource(self, args: pulumi.runtime.MockResourceArgs):
        return [args.name + '_id', args.inputs]

    def call(self, args: pulumi.runtime.MockCallArgs):
        return {}


pulumi.runtime.set_mocks(MyMocks())

import infra


class TestingWithMocks(unittest.TestCase):

    # Test template.
    @pulumi.runtime.test
    def test_template(self) -> pulumi.Output:
        def check_template(args: list) -> None:
            _, = args
            assert ..., 'Template error message.'

        return pulumi.Output.all(infra).apply(check_template)

    # Test that the bucket URN matches the resource name of the bucket.
    @pulumi.runtime.test
    def test_bucket_urn_correctness(self) -> pulumi.Output:
        bucket = infra.create_bucket()

        def check_bucket_urn(args: list) -> None:
            urn, = args
            bucket_name = urn.split('::')[-1]
            assert bucket_name == infra.BUCKET_NAME

        return pulumi.Output.all(bucket.urn).apply(check_bucket_urn)
