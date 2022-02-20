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
