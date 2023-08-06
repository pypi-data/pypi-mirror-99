from enoslib.service.netem.netem import (
    _build_commands,
    _build_ip_constraints,
    _expand_description,
    _generate_default_grp_constraints,
    _generate_actual_grp_constraints,
    _build_grp_constraints,
    _merge_constraints,
)
from enoslib.host import Host
from enoslib.tests.unit import EnosTest


class TestExpandDescription(EnosTest):
    def test_no_expansion(self):
        desc = {"src": "grp1", "dst": "grp2", "delay": 0, "rate": 0, "symetric": True}
        descs = _expand_description(desc)
        self.assertEqual(1, len(descs))
        self.assertDictEqual(desc, descs[0])

    def test_src_expansion(self):
        desc = {
            "src": "grp[1-3]",
            "dst": "grp4",
            "delay": 0,
            "rate": 0,
            "symetric": True,
        }
        # checking cardinality : the cartesian product
        descs = _expand_description(desc)
        self.assertEqual(3, len(descs))

        # checking that expansion has been generated
        srcs = map(lambda d: d.pop("src"), descs)
        self.assertEqual(set(srcs), {"grp1", "grp2", "grp3"})

        # checking that the remaining is untouched
        desc.pop("src")
        for d in descs:
            self.assertDictEqual(desc, d)

    def test_dst_expansion(self):
        desc = {
            "src": "grp4",
            "dst": "grp[1-3]",
            "delay": 0,
            "rate": 0,
            "symetric": True,
        }
        # checking cardinality : the cartesian product
        descs = _expand_description(desc)
        self.assertEqual(3, len(descs))

        # checking that expansion has been generated
        dsts = map(lambda d: d.pop("dst"), descs)
        self.assertEqual(set(dsts), {"grp1", "grp2", "grp3"})

        # checking that the remaining is untouched
        desc.pop("dst")
        for d in descs:
            self.assertDictEqual(desc, d)

    def test_both_expansion(self):
        desc = {
            "src": "grp[1-3]",
            "dst": "grp[4-6]",
            "delay": 0,
            "rate": 0,
            "symetric": True,
        }
        # checking cardinality : the cartesian product
        descs = _expand_description(desc)
        self.assertEqual(9, len(descs))

        # checking that expansion has been generated
        dsts = map(lambda d: d.pop("dst"), descs)
        self.assertEqual(set(dsts), {"grp4", "grp5", "grp6"})
        # checking that expansion has been generated
        srcs = map(lambda d: d.pop("src"), descs)
        self.assertEqual(set(srcs), {"grp1", "grp2", "grp3"})

        # checking that the remaining is untouched
        desc.pop("dst")
        desc.pop("src")
        for d in descs:
            self.assertDictEqual(desc, d)


class TestGenerateDefaultGrpConstraints(EnosTest):
    def test_no_expansion(self):
        roles = {"grp1": [], "grp2": []}
        network_constraints = {"default_rate": "10mbit", "default_delay": "10ms"}
        descs = _generate_default_grp_constraints(roles, network_constraints)

        # Cartesian product is applied
        self.assertEqual(2, len(descs))

        # defaults are applied
        for d in descs:
            self.assertEqual("10mbit", d["rate"])
            self.assertEqual("10ms", d["delay"])

        # descs are symetrics
        self.assertEqual(descs[0]["src"], descs[1]["dst"])
        self.assertEqual(descs[0]["dst"], descs[1]["src"])

    def test_except_one_group(self):
        roles = {"grp1": [], "grp2": [], "grp3": []}
        network_constraints = {
            "default_rate": "10mbit",
            "default_delay": "10ms",
            "except": ["grp1"],
        }
        descs = _generate_default_grp_constraints(roles, network_constraints)
        # Cartesian product is applied but grp1 isn't taken
        self.assertEqual(2, len(descs))

        for d in descs:
            self.assertTrue("grp1" != d["src"])
            self.assertTrue("grp1" != d["dst"])

    def test_include_two_groups(self):
        roles = {"grp1": [], "grp2": [], "grp3": []}
        network_constraints = {
            "default_rate": "10mbit",
            "default_delay": "10ms",
            "groups": ["grp2", "grp3"],
        }
        descs = _generate_default_grp_constraints(roles, network_constraints)

        # Cartesian product is applied but grp1 isn't taken
        self.assertEqual(2, len(descs))

        for d in descs:
            self.assertTrue("grp1" != d["src"])
            self.assertTrue("grp1" != d["dst"])


class TestGenerateActualGrpConstraints(EnosTest):
    def test_no_expansion_no_symetric(self):
        constraints = [
            {"src": "grp1", "dst": "grp2", "rate": "20mbit", "delay": "20ms"}
        ]
        network_constraints = {
            "default_rate": "10mbit",
            "default_delay": "10ms",
            "constraints": constraints,
        }
        descs = _generate_actual_grp_constraints(network_constraints)

        self.assertEqual(1, len(descs))
        self.assertDictEqual(constraints[0], descs[0])

    def test_no_expansion_symetric(self):
        constraints = [
            {
                "src": "grp1",
                "dst": "grp2",
                "rate": "20mbit",
                "delay": "20ms",
                "symetric": True,
            }
        ]
        network_constraints = {
            "default_rate": "10mbit",
            "default_delay": "10ms",
            "constraints": constraints,
        }
        descs = _generate_actual_grp_constraints(network_constraints)

        self.assertEqual(2, len(descs))

        # bw/rate are applied
        for d in descs:
            self.assertEqual("20mbit", d["rate"])
            self.assertEqual("20ms", d["delay"])

        # descs are symetrics
        self.assertEqual(descs[0]["src"], descs[1]["dst"])
        self.assertEqual(descs[0]["dst"], descs[1]["src"])

    def test_expansion_symetric(self):
        constraints = [
            {
                "src": "grp[1-3]",
                "dst": "grp[4-6]",
                "rate": "20mbit",
                "delay": "20ms",
                "symetric": True,
            }
        ]
        network_constraints = {
            "default_rate": "10mbit",
            "default_delay": "10ms",
            "constraints": constraints,
        }
        descs = _generate_actual_grp_constraints(network_constraints)

        self.assertEqual(3 * 3 * 2, len(descs))

        # bw/rate are applied
        for d in descs:
            self.assertEqual("20mbit", d["rate"])
            self.assertEqual("20ms", d["delay"])

    def test_expansion_no_symetric(self):
        constraints = [
            {"src": "grp[1-3]", "dst": "grp[4-6]", "rate": "20mbit", "delay": "20ms"}
        ]
        network_constraints = {
            "default_rate": "10mbit",
            "default_delay": "10ms",
            "constraints": constraints,
        }
        descs = _generate_actual_grp_constraints(network_constraints)

        self.assertEqual(3 * 3, len(descs))

        # bw/rate are applied
        for d in descs:
            self.assertEqual("20mbit", d["rate"])
            self.assertEqual("20ms", d["delay"])

    def test_same_src_and_dest_defaults_embedded(self):
        constraints = [
            {"src": "grp1", "dst": "grp1", "rate": "20mbit", "delay": "20ms"}
        ]
        network_constraints = {
            "default_rate": "10mbit",
            "default_delay": "10ms",
            "constraints": constraints,
        }
        descs = _generate_actual_grp_constraints(network_constraints)

        self.assertEqual(1, len(descs))
        self.assertDictEqual(constraints[0], descs[0])
        for d in descs:
            self.assertTrue("grp1" == d["src"])
            self.assertTrue("grp1" == d["dst"])

    def test_same_src_and_dest_without_defaults(self):
        roles = {"grp1": [Host("node1")], "grp2": [Host("node2")]}
        constraints = [{"src": "grp1", "dst": "grp1"}]
        network_constraints = {
            "default_rate": "10mbit",
            "default_delay": "10ms",
            "constraints": constraints,
        }
        descs = _build_grp_constraints(roles, network_constraints)
        self.assertEqual(3, len(descs))
        # bw/rate are applied
        count_src_equals_dst = 0
        for d in descs:
            self.assertEqual("10mbit", d["rate"])
            self.assertEqual("10ms", d["delay"])
            if d["src"] == d["dst"] == "grp1":
                count_src_equals_dst += 1
        self.assertEqual(1, count_src_equals_dst)


class TestMergeConstraints(EnosTest):
    def test__merge_constraints(self):
        constraint = {"src": "grp1", "dst": "grp2", "rate": "10mbit", "delay": "10ms"}
        constraints = [constraint]
        override = {"src": "grp1", "dst": "grp2", "rate": "20mbit", "delay": "20ms"}
        overrides = [override]
        _merge_constraints(constraints, overrides)
        self.assertDictEqual(override, constraints[0])

    def test__merge_constraints_default(self):
        constraint = {"src": "grp1", "dst": "grp2", "rate": "10mbit", "delay": "10ms"}
        constraints = [constraint]
        override = {"src": "grp1", "dst": "grp2", "rate": "20mbit"}
        overrides = [override]
        _merge_constraints(constraints, overrides)

        override.update({"delay": "10ms"})
        self.assertDictEqual(override, constraints[0])


class TestBuildIpConstraints(EnosTest):
    def setUp(self):
        self.n1 = Host("node1")
        self.n2 = Host("node2")
        self.rsc = {"grp1": [self.n1], "grp2": [self.n2]}
        constraint = {
            "src": "grp1",
            "dst": "grp2",
            "rate": "10mbit",
            "delay": "10ms",
            "loss": "0.1%",
        }
        self.constraints = [constraint]
        self.ips = {
            "node1": {
                "all_ipv4_addresses": ["ip11", "ip12"],
                "devices": [
                    {"device": "eth0", "active": True, "type": "ether"},
                    {"device": "eth1", "active": True, "type": "ether"},
                ],
                "enos_devices": ["eth0", "eth1"],
            },
            "node2": {
                "all_ipv4_addresses": ["ip21", "ip21"],
                "devices": [
                    {"device": "eth0", "active": True, "type": "ether"},
                    {"device": "eth1", "active": True, "type": "ether"},
                ],
                "enos_devices": ["eth0", "eth1"],
            },
        }

        self.ips_with_bridge = {
            "node1": {
                "all_ipv4_addresses": ["ip11", "ip12"],
                "devices": [
                    {"device": "eth0", "active": True, "type": "ether"},
                    {
                        "device": "br0",
                        "active": True,
                        "type": "bridge",
                        "interfaces": ["eth0"],
                    },
                ],
                "enos_devices": ["br0"],
            },
            "node2": {
                "all_ipv4_addresses": ["ip21", "ip22"],
                "devices": [
                    {"device": "eth0", "active": True, "type": "ether"},
                    {
                        "device": "br0",
                        "active": True,
                        "type": "bridge",
                        "interfaces": ["eth0"],
                    },
                ],
                "enos_devices": ["br0"],
            },
        }

    def test_build_ip_constraints(self):
        ips_with_tc = _build_ip_constraints(self.rsc, self.ips, self.constraints)
        # tc rules are applied on the source only
        self.assertFalse("node2" in ips_with_tc)
        # devices
        self.assertTrue("devices" in ips_with_tc["node1"])
        self.assertEqual(2, len(ips_with_tc["node1"]["devices"]))
        self.assertTrue("tc" in ips_with_tc["node1"])
        tcs = ips_with_tc["node1"]["tc"]
        # one rule per dest ip and source device
        self.assertEqual(2 * 2, len(tcs))

    def test_build_ip_constraints_bridge(self):
        ips_with_tc = _build_ip_constraints(
            self.rsc, self.ips_with_bridge, self.constraints
        )
        # tc rules are applied on the source only
        self.assertTrue("tc" in ips_with_tc["node1"])
        tcs = ips_with_tc["node1"]["tc"]
        # one rule per dest ip and source device
        self.assertEqual(1 * 2, len(tcs))
        # br0 isn't use but eth0 is
        devices = set()
        for tc in tcs:
            devices.add(tc["device"])
        self.assertCountEqual(["eth0"], list(devices))

    def test_build_commands(self):
        self.constraints[0]["symetric"] = True
        ips_with_tc = _build_ip_constraints(self.rsc, self.ips, self.constraints)
        remove, add, rate, delay, filtr = _build_commands(ips_with_tc)
        self.assertEqual(2, len(remove[self.n1]))
        # symetric cases are handled prior to _build_ip_constraints
        # so are we aren't symetric unless we add a symetric constraint
        self.assertEqual(0, len(remove[self.n2]))
        self.assertEqual(2, len(add[self.n1]))
        self.assertEqual(0, len(add[self.n2]))
        # we have as many rate class as possible (device, dest)
        self.assertEqual(2 * 2, len(rate[self.n1]))
        # delay
        self.assertEqual(2 * 2, len(delay[self.n1]))
        # we put filter on every (device, dest) possible
        self.assertEqual(2 * 2, len(filtr[self.n1]))
