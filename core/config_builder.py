#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string
from core._time import now


def all_profiles():
    return {
        "information_gathering": ["tcp_connect_port_scan"],
        "vulnerabilities": ["heartbleed_vuln"]
    }


def all_config_keys():
    return {
        "language": "en",
        "verbose_level": 0,
        "show_version": False,
        "check_update": False,
        "log_in_file": "results/results_{0}_{1}.html".format(now(model="%Y_%m_%d_%H_%M_%S"),
                                                             ''.join(random.choice(string.ascii_lowercase) for x in
                                                                     range(10))),
        "graph_flag": "d3_tree_v2_graph",
        "help_menu_flag": False,
        "targets": None,
        "targets_list": None,
        "scan_method": "all",
        "exclude_method": None,
        "users": None,
        "users_list": None,
        "passwds": None,
        "passwds_list": None,
        "ports": None,
        "timeout_sec": 2.0,
        "time_sleep": 0.0,
        "check_ranges": False,
        "check_subdomains": False,
        "thread_number": 10,
        "thread_number_host": 10,
        "socks_proxy": None,
        "retries": 3,
        "ping_flag": False,
        "methods_args": None,
        "method_args_list": False,
        "startup_check_for_update": True,
        "wizard_mode": False,
        "profile": None
    }


def _builder(defaults, keys):
    for key in keys:
        try:
            defaults[key]
        except:
            defaults[key] = keys[key]
    return defaults
