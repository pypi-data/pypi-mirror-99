# Copyright (C) 2015 Catalyst IT Ltd
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.test import TestCase
from rest_framework.test import APITestCase

from adjutant.common.tests import fake_clients


class AdjutantTestCase(TestCase):
    def tearDown(self):
        fake_clients.identity_cache.clear()
        fake_clients.neutron_cache.clear()
        fake_clients.nova_cache.clear()
        fake_clients.cinder_cache.clear()


class AdjutantAPITestCase(APITestCase):
    def tearDown(self):
        fake_clients.identity_cache.clear()
        fake_clients.neutron_cache.clear()
        fake_clients.nova_cache.clear()
        fake_clients.cinder_cache.clear()
