# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
test_compute
----------------------------------

Functional tests for `shade` compute methods.
"""

from shade import openstack_cloud
from shade.tests import base
from shade.tests.functional.util import pick_flavor, pick_image


class TestCompute(base.TestCase):
    def setUp(self):
        super(TestCompute, self).setUp()
        self.cloud = openstack_cloud(cloud='devstack')
        self.flavor = pick_flavor(self.cloud.list_flavors())
        if self.flavor is None:
            self.assertFalse('no sensible flavor available')
        self.image = pick_image(self.cloud.list_images())
        if self.image is None:
            self.assertFalse('no sensible image available')

    def _cleanup_servers(self):
        for i in self.cloud.list_servers():
            if i.name.startswith('test_create'):
                self.cloud.delete_server(i)

    def test_create_server(self):
        self.addCleanup(self._cleanup_servers)
        server = self.cloud.create_server(name='test_create_server',
                                          image=self.image, flavor=self.flavor)
        self.assertEquals(server['name'], 'test_create_server')
        self.assertEquals(server['image']['id'], self.image.id)
        self.assertEquals(server['flavor']['id'], self.flavor.id)

    def test_delete_server(self):
        self.cloud.create_server(name='test_delete_server',
                                 image=self.image, flavor=self.flavor)
        server_deleted = self.cloud.delete_server('test_delete_server',
                                                  wait=True)
        self.assertIsNone(server_deleted)

    def test_get_image_id(self):
        self.assertEqual(
            self.image.id, self.cloud.get_image_id(self.image.id))
        self.assertEqual(
            self.image.id, self.cloud.get_image_id(self.image.name))

    def test_get_image_name(self):
        self.assertEqual(
            self.image.name, self.cloud.get_image_name(self.image.id))
        self.assertEqual(
            self.image.name, self.cloud.get_image_name(self.image.name))
