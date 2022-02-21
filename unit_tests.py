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
        bucket, _ = infra.create_bucket_and_object()

        def check_bucket_urn(args: list) -> None:
            urn, = args
            bucket_name = urn.split('::')[-1]
            assert bucket_name == infra.BUCKET_NAME

        return pulumi.Output.all(bucket.urn).apply(check_bucket_urn)

    # Test that the bucket has a website property.
    @pulumi.runtime.test
    def test_bucket_website_property(self) -> pulumi.Output:
        bucket, _ = infra.create_bucket_and_object()

        def check_website_property(args: list) -> None:
            website, = args
            assert website is not None

        return pulumi.Output.all(bucket.website).apply(check_website_property)

    # Test that the website bucket object has content type HTML.
    @pulumi.runtime.test
    def test_website_content_type(self) -> pulumi.Output:
        _, bucket_object = infra.create_bucket_and_object()

        def check_website_content(args: list) -> None:
            content_type, = args
            assert content_type == infra.HTML_CONTENT

        return pulumi.Output.all(bucket_object.content_type).apply(
            check_website_content)
