import mock
from netaddr import EUI

from enoslib.host import Host
from enoslib.infra.enos_vmong5k.configuration import Configuration, MachineConfiguration
from enoslib.infra.enos_vmong5k.provider import (
    _do_build_g5k_conf,
    _distribute,
    _index_by_host,
    VirtualMachine,
)
from enoslib.tests.unit import EnosTest


class TestBuildG5kConf(EnosTest):
    @mock.patch(
        "enoslib.infra.enos_vmong5k.provider._find_nodes_number", return_value=2
    )
    @mock.patch(
        "enoslib.infra.enos_g5k.configuration.get_cluster_site", return_value="site1"
    )
    def test_do_build_g5k_conf(self, mock_get_cluster_site, mock_find_node_number):
        conf = Configuration()
        conf.add_machine(roles=["r1"], cluster="cluster1", number=10, flavour="tiny")
        conf.finalize()
        g5k_conf = _do_build_g5k_conf(conf, "rennes")
        # it's valid
        g5k_conf.finalize()

        # machines
        self.assertEqual(1, len(g5k_conf.machines))
        machine = g5k_conf.machines[0]
        self.assertEqual("cluster1", machine.cluster)
        self.assertEqual(2, machine.nodes)
        # role have been expanded with the unique cookie
        self.assertEqual(2, len(machine.roles))

        # networks
        self.assertEqual(2, len(g5k_conf.networks))
        self.assertTrue(g5k_conf.networks[0].type in ["prod", "slash_22"])
        self.assertTrue(g5k_conf.networks[1].type in ["prod", "slash_22"])


class TestDistribute(EnosTest):
    def test_distribute_minimal(self):

        host = Host("paravance-1")
        machine = MachineConfiguration(
            roles=["r1"], flavour="tiny", undercloud=[host], number=1
        )
        machines = [machine]

        g5k_subnet = {"mac_start": "00:16:3E:9E:44:00", "mac_end": "00:16:3E:9E:47:FE"}

        vmong5k_roles = _distribute(machines, [g5k_subnet])
        self.assertEqual(1, len(vmong5k_roles["r1"]))
        vm = vmong5k_roles["r1"][0]
        # we skip the first mac
        self.assertEqual(EUI(int(EUI(g5k_subnet["mac_start"])) + 1), vm.eui)
        self.assertEqual(host, vm.pm)

    def test_distribute_minimal_skip(self):

        host = Host("paravance-1")
        machine = MachineConfiguration(
            roles=["r1"], flavour="tiny", undercloud=[host], number=1
        )
        machines = [machine]

        g5k_subnet = {"mac_start": "00:16:3E:9E:44:00", "mac_end": "00:16:3E:9E:47:FE"}

        vmong5k_roles = _distribute(machines, [g5k_subnet], skip=10)
        self.assertEqual(1, len(vmong5k_roles["r1"]))
        vm = vmong5k_roles["r1"][0]
        # we skip the first mac + 10 more
        self.assertEqual(EUI(int(EUI(g5k_subnet["mac_start"])) + 11), vm.eui)
        self.assertEqual(host, vm.pm)

    def test_distribute_2_vms_1_host(self):
        host = Host("paravance-1")
        machine = MachineConfiguration(
            roles=["r1"], flavour="tiny", undercloud=[host], number=2
        )
        machines = [machine]

        g5k_subnet = {"mac_start": "00:16:3E:9E:44:00", "mac_end": "00:16:3E:9E:47:FE"}

        vmong5k_roles = _distribute(machines, [g5k_subnet])
        self.assertEqual(2, len(vmong5k_roles["r1"]))
        vm = vmong5k_roles["r1"][0]
        # we skip the first mac
        self.assertEqual(EUI(int(EUI(g5k_subnet["mac_start"])) + 1), vm.eui)
        self.assertEqual(host, vm.pm)

        vm = vmong5k_roles["r1"][1]
        self.assertEqual(EUI(int(EUI(g5k_subnet["mac_start"])) + 2), vm.eui)
        self.assertEqual(host, vm.pm)

    def test_distribute_2_vms_2_hosts(self):
        host0 = Host("paravance-1")
        host1 = Host("paravance-2")
        machine = MachineConfiguration(
            roles=["r1"], flavour="tiny", undercloud=[host0, host1], number=2
        )
        machines = [machine]

        g5k_subnet = {
            "mac_start": EUI("00:16:3E:9E:44:00"),
            "mac_end": EUI("00:16:3E:9E:47:FE"),
        }

        vmong5k_roles = _distribute(machines, [g5k_subnet])
        self.assertEqual(2, len(vmong5k_roles["r1"]))
        vm = vmong5k_roles["r1"][0]
        # we skip the first mac
        self.assertEqual(EUI(int(g5k_subnet["mac_start"]) + 1), vm.eui)
        self.assertEqual(host0, vm.pm)

        vm = vmong5k_roles["r1"][1]
        self.assertEqual(EUI(int(g5k_subnet["mac_start"]) + 2), vm.eui)
        self.assertEqual(host1, vm.pm)
