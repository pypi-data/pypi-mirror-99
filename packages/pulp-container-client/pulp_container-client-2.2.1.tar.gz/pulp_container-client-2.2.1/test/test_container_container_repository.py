# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_container
from pulpcore.client.pulp_container.models.container_container_repository import ContainerContainerRepository  # noqa: E501
from pulpcore.client.pulp_container.rest import ApiException

class TestContainerContainerRepository(unittest.TestCase):
    """ContainerContainerRepository unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ContainerContainerRepository
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_container.models.container_container_repository.ContainerContainerRepository()  # noqa: E501
        if include_optional :
            return ContainerContainerRepository(
                name = '0', 
                description = '0', 
                remote = '0'
            )
        else :
            return ContainerContainerRepository(
                name = '0',
        )

    def testContainerContainerRepository(self):
        """Test ContainerContainerRepository"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
