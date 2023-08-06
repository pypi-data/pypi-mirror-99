# Copyright 2020 Red Hat, Inc.
# All Rights Reserved.
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

from unittest import mock

from oslo_config import cfg

from kuryr_kubernetes.controller.drivers import node_subnets
from kuryr_kubernetes import exceptions
from kuryr_kubernetes.tests import base as test_base


class TestConfigNodesSubnetsDriver(test_base.TestCase):

    def test_get_nodes_subnets(self):
        subnets = ['subnet1', 'subnet2']
        cfg.CONF.set_override('worker_nodes_subnets', subnets,
                              group='pod_vif_nested')
        driver = node_subnets.ConfigNodesSubnets()

        self.assertEqual(subnets, driver.get_nodes_subnets())

    def test_get_nodes_subnets_alias(self):
        subnet = 'subnet1'
        cfg.CONF.set_override('worker_nodes_subnet', subnet,
                              group='pod_vif_nested')
        driver = node_subnets.ConfigNodesSubnets()

        self.assertEqual([subnet], driver.get_nodes_subnets())

    def test_get_project_not_set_raise(self):
        cfg.CONF.set_override('worker_nodes_subnets', None,
                              group='pod_vif_nested')
        driver = node_subnets.ConfigNodesSubnets()

        self.assertRaises(cfg.RequiredOptError, driver.get_nodes_subnets,
                          raise_on_empty=True)

    def test_get_project_not_set(self):
        cfg.CONF.set_override('worker_nodes_subnets', None,
                              group='pod_vif_nested')
        driver = node_subnets.ConfigNodesSubnets()

        self.assertEqual([], driver.get_nodes_subnets())

    def test_add_node(self):
        driver = node_subnets.ConfigNodesSubnets()
        self.assertFalse(driver.add_node('node'))

    def test_delete_node(self):
        driver = node_subnets.ConfigNodesSubnets()
        self.assertFalse(driver.delete_node('node'))


class TestOpenShiftNodesSubnetsDriver(test_base.TestCase):
    def setUp(self):
        super().setUp()
        self.machine = {
            "apiVersion": "machine.openshift.io/v1beta1",
            "kind": "Machine",
            "metadata": {
                "name": "foo-tv22d-master-2",
                "namespace": "openshift-machine-api",
            },
            "spec": {
                "metadata": {},
                "providerSpec": {
                    "value": {
                        "cloudName": "openstack",
                        "cloudsSecret": {
                            "name": "openstack-cloud-credentials",
                            "namespace": "openshift-machine-api"
                        },
                        "kind": "OpenstackProviderSpec",
                        "networks": [
                            {
                                "filter": {},
                                "subnets": [{
                                    "filter": {
                                        "name": "foo-tv22d-nodes",
                                        "tags": "openshiftClusterID=foo-tv22d"
                                    }}
                                ]
                            }
                        ],
                    }
                }
            },
            "status": {}
        }
        cfg.CONF.set_override('worker_nodes_subnets', [],
                              group='pod_vif_nested')

    def test_get_nodes_subnets(self):
        subnets = ['subnet1', 'subnet2']
        driver = node_subnets.OpenShiftNodesSubnets()
        for subnet in subnets:
            driver.subnets.add(subnet)
        self.assertCountEqual(subnets, driver.get_nodes_subnets())

    def test_get_nodes_subnets_with_config(self):
        subnets = ['subnet1', 'subnet2']
        cfg.CONF.set_override('worker_nodes_subnets', ['subnet3', 'subnet2'],
                              group='pod_vif_nested')
        driver = node_subnets.OpenShiftNodesSubnets()
        for subnet in subnets:
            driver.subnets.add(subnet)
        self.assertCountEqual(['subnet1', 'subnet2', 'subnet3'],
                              driver.get_nodes_subnets())

    def test_get_nodes_subnets_not_raise(self):
        driver = node_subnets.OpenShiftNodesSubnets()
        self.assertEqual([], driver.get_nodes_subnets())

    def test_get_nodes_subnets_raise(self):
        driver = node_subnets.OpenShiftNodesSubnets()
        self.assertRaises(exceptions.ResourceNotReady,
                          driver.get_nodes_subnets, raise_on_empty=True)

    @mock.patch('kuryr_kubernetes.utils.get_subnet_id')
    def test_add_node(self, m_get_subnet_id):
        driver = node_subnets.OpenShiftNodesSubnets()
        m_get_subnet_id.return_value = 'foobar'
        self.assertTrue(driver.add_node(self.machine))
        m_get_subnet_id.assert_called_once_with(
            name='foo-tv22d-nodes', tags='openshiftClusterID=foo-tv22d')
        self.assertEqual(['foobar'], driver.get_nodes_subnets())

    @mock.patch('kuryr_kubernetes.utils.get_subnet_id')
    def test_add_node_exists(self, m_get_subnet_id):
        driver = node_subnets.OpenShiftNodesSubnets()
        m_get_subnet_id.return_value = 'foobar'
        driver.subnets.add('foobar')
        self.assertFalse(driver.add_node(self.machine))
        m_get_subnet_id.assert_called_once_with(
            name='foo-tv22d-nodes', tags='openshiftClusterID=foo-tv22d')
        self.assertEqual(['foobar'], driver.get_nodes_subnets())

    @mock.patch('kuryr_kubernetes.utils.get_subnet_id')
    def test_add_node_uuid(self, m_get_subnet_id):
        driver = node_subnets.OpenShiftNodesSubnets()
        net = self.machine['spec']['providerSpec']['value']['networks'][0]
        del net['subnets'][0]['filter']
        net['subnets'][0]['uuid'] = 'barfoo'
        self.assertTrue(driver.add_node(self.machine))
        m_get_subnet_id.assert_not_called()
        self.assertEqual(['barfoo'], driver.get_nodes_subnets())

    @mock.patch('kuryr_kubernetes.utils.get_subnet_id')
    def test_add_node_cannot(self, m_get_subnet_id):
        driver = node_subnets.OpenShiftNodesSubnets()
        net = self.machine['spec']['providerSpec']['value']['networks'][0]
        del net['subnets']
        self.assertFalse(driver.add_node(self.machine))
        m_get_subnet_id.assert_not_called()
        self.assertEqual([], driver.get_nodes_subnets())

    @mock.patch('kuryr_kubernetes.utils.get_subnet_id')
    @mock.patch('kuryr_kubernetes.clients.get_kubernetes_client')
    def test_delete_node_cannot(self, m_get_k8s, m_get_subnet_id):
        m_k8s = mock.Mock()
        m_get_k8s.return_value = m_k8s
        driver = node_subnets.OpenShiftNodesSubnets()
        net = self.machine['spec']['providerSpec']['value']['networks'][0]
        del net['subnets']
        self.assertFalse(driver.delete_node(self.machine))
        m_get_subnet_id.assert_not_called()
        self.assertEqual([], driver.get_nodes_subnets())

    @mock.patch('kuryr_kubernetes.utils.get_subnet_id')
    @mock.patch('kuryr_kubernetes.clients.get_kubernetes_client')
    def test_delete_node(self,  m_get_k8s, m_get_subnet_id):
        m_k8s = mock.Mock()
        m_get_k8s.return_value = m_k8s
        m_k8s.get.return_value = {'items': []}

        driver = node_subnets.OpenShiftNodesSubnets()
        driver.subnets.add('foobar')
        m_get_subnet_id.return_value = 'foobar'
        self.assertTrue(driver.delete_node(self.machine))
        m_get_subnet_id.assert_called_once_with(
            name='foo-tv22d-nodes', tags='openshiftClusterID=foo-tv22d')
        self.assertEqual([], driver.get_nodes_subnets())

    @mock.patch('kuryr_kubernetes.utils.get_subnet_id')
    @mock.patch('kuryr_kubernetes.clients.get_kubernetes_client')
    def test_delete_node_still_exists(self,  m_get_k8s, m_get_subnet_id):
        m_k8s = mock.Mock()
        m_get_k8s.return_value = m_k8s
        m_k8s.get.return_value = {'items': [self.machine]}

        driver = node_subnets.OpenShiftNodesSubnets()
        driver.subnets.add('foobar')
        m_get_subnet_id.return_value = 'foobar'
        self.assertFalse(driver.delete_node(self.machine))
        m_get_subnet_id.assert_called_with(
            name='foo-tv22d-nodes', tags='openshiftClusterID=foo-tv22d')
        self.assertEqual(['foobar'], driver.get_nodes_subnets())
