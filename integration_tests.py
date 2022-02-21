import os
import unittest

from pulumi import automation as auto

from infra import OUTPUT_KEY_REGION

STACK_NAME = 'Staging'
REGION_NAME = 'eu-north-1'


class TestS3(unittest.TestCase):
    stack = None

    @classmethod
    def setUpClass(cls) -> None:
        # Set up test stack
        work_directory = os.path.join(os.path.dirname(__file__))
        stack_kwargs = dict(stack_name=STACK_NAME, work_dir=work_directory)
        cls.stack = auto.create_or_select_stack(**stack_kwargs)

        # Configure region for test stack
        region_value = auto.ConfigValue(value=REGION_NAME)
        cls.stack.set_config("aws:region", region_value)

        # Configure test stack output
        cls.stack.up(on_output=print)
        cls.outputs = cls.stack.outputs()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.stack.destroy(on_output=print)
        cls.stack.workspace.remove_stack(STACK_NAME)

    def test_output_region(self):
        output_region = self.outputs.get(OUTPUT_KEY_REGION)
        assert REGION_NAME == output_region.value


if __name__ == '__main__':
    unittest.main()
