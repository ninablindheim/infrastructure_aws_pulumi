import os
import unittest

import boto3
from pulumi import automation as auto

import infra


class TestS3(unittest.TestCase):
    stack: auto.Stack = None

    @classmethod
    def setUpClass(cls) -> None:
        # Set up test stack
        working_directory = os.path.join(os.path.dirname(__file__))
        cls.stack = auto.create_or_select_stack(
            stack_name=infra.STACK_NAME, work_dir=working_directory)

        # Configure region for test stack
        region_value = auto.ConfigValue(value=infra.REGION_NAME)
        cls.stack.set_config(infra.CONFIG_KEY_REGION, region_value)

        # Configure test stack output
        cls.stack.up(on_output=print)
        cls.outputs = cls.stack.outputs()
        cls.s3 = boto3.resource('s3')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.stack.destroy(on_output=print)
        cls.stack.workspace.remove_stack(infra.STACK_NAME)

    # Test that the output name matches the bucket name.
    def test_output_name(self):
        output_name = self.outputs.get(infra.OUTPUT_KEY_BUCKET_NAME)
        stripped_name = '-'.join(output_name.value.split('-')[:-1])
        assert stripped_name == infra.BUCKET_NAME

    # Test that the output region matches the region name.
    def test_output_region(self):
        output_region = self.outputs.get(infra.OUTPUT_KEY_REGION)
        assert output_region.value == infra.REGION_NAME

    # Test that the bucket exists.
    def test_bucket_existence(self):
        output_name = self.outputs.get(infra.OUTPUT_KEY_BUCKET_NAME).value
        bucket_names = [bucket.name for bucket in self.s3.buckets.all()]
        assert output_name in bucket_names


if __name__ == '__main__':
    unittest.main()
