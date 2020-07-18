#!/usr/bin/env python3
#
# Copyright 2017 Nicholas de Jong  <contact[at]nicholasdejong.com>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 

import os, sys, json
try:
    from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi
except:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi


def usage():
    print()
    print('usage: ' + sys.argv[0] + ' <host>')
    print()
    print('  Environment variables containing credentials MUST be set before use!')
    print('    $ export FAUXAPI_APIKEY=PFFAyourkeyvalue')
    print('    $ export FAUXAPI_APISECRET=devtrashdevtrashdevtrashdevtrashdevtrash')
    print()
    print('pipe JSON output through jq for easy pretty print output:-')
    print(' $ ' + sys.argv[0] + ' <host> | jq .')
    print()
    sys.exit(1)


# check args and env exist
if(len(sys.argv) != 2) or not os.getenv('FAUXAPI_APIKEY') or not os.getenv('FAUXAPI_APISECRET'):
    usage()

# config
fauxapi_host=sys.argv[1]
fauxapi_apikey=os.getenv('FAUXAPI_APIKEY')
fauxapi_apisecret=os.getenv('FAUXAPI_APISECRET')


FauxapiLib = PfsenseFauxapi(fauxapi_host, fauxapi_apikey, fauxapi_apisecret, debug=False)


# config get the full configuration and simply print to console
# =============================================================================
config = FauxapiLib.config_get()
print(json.dumps(
    config
))

# config set the full configuration
# =============================================================================
# NB: nothing amazing is happening here, we are simply writing back the same (full) configuration again, the developer
# most likely wants to make changes to `config` before calling the config_set function again here
print(json.dumps(
    FauxapiLib.config_set(config)
))

# config_get, config_set by section
# =============================================================================
# perform a second config_get > config_set this time within the 'aliases' section only
# NB: again, nothing amazing happening in this example, we are are again only writing back the same (section)
# configuration, the developer more likely wants to perform some kind of operation on `config_aliases` before calling
# the config_set function again.
config_aliases = FauxapiLib.config_get('aliases')
print(json.dumps(
    FauxapiLib.config_set(config_aliases, 'aliases'))
)

# config_patch
# =============================================================================
# in this example we patch a specific set of configuration parameters and then revert them back to what they were
config_patch = {
    'system': {
        'dnsserver': ['8.8.8.8', '8.8.4.4'],
        'hostname': 'testing'
    }
}
print(json.dumps(
    FauxapiLib.config_patch(config_patch)
))

# config_patch - set dnsserver to what it was originally
config_patch = {
    'system': {
        'dnsserver': config['system']['dnsserver'] if 'dnsserver' in config['system'] else [''],
        'hostname': config['system']['hostname'],
    }
}
print(json.dumps(
    FauxapiLib.config_patch(config_patch)
))

# config get the full configuration again so we can manually confirm it has been restored
config = FauxapiLib.config_get()
print(json.dumps(
    config
))

# config reload
# =============================================================================
print(json.dumps(
    FauxapiLib.config_reload())
)

# config backuo
# =============================================================================
print(json.dumps(
    FauxapiLib.config_backup())
)

# config_backup_list
# =============================================================================
print(json.dumps(
    FauxapiLib.config_backup_list())
)

# # config_restore
# =============================================================================
# print(json.dumps(
#     FauxapiLib.config_restore('/cf/conf/backup/config-1530604754.xml'))
# )

# system_stats
# =============================================================================
print(json.dumps(
    FauxapiLib.system_stats())
)

# interface_stats - NB: the real interface name, not an interface alias such as "WAN" or "LAN"
# =============================================================================
print(json.dumps(
    FauxapiLib.interface_stats('em0'))
)

# gateway_status
# =============================================================================
print(json.dumps(
    FauxapiLib.gateway_status())
)

# send_event - filter reload
# =============================================================================
print(json.dumps(
    FauxapiLib.send_event('filter reload'))
)

# send_event - interface all reload
# =============================================================================
print(json.dumps(
    FauxapiLib.send_event('interface all reload'))
)

# rule_get - get all rules
# =============================================================================
print(json.dumps(
    FauxapiLib.rule_get())
)

# rule_get - get rule number 5
# =============================================================================
print(json.dumps(
    FauxapiLib.rule_get(5))
)

# alias_update_urltables
# =============================================================================
print(json.dumps(
    FauxapiLib.alias_update_urltables())
)

# # system reboot
# =============================================================================
# print(json.dumps(
#     FauxapiLib.system_reboot())
# )

# function_call - examples
# =============================================================================
print(json.dumps(
    FauxapiLib.function_call({
        'function': 'return_gateways_status',
        'args': [False]
    }
)))

print(json.dumps(
    FauxapiLib.function_call({
        'function': 'discover_last_backup'
    }
)))

print(json.dumps(
    FauxapiLib.function_call({
        'function': 'return_gateways_status',
        'includes': ['gwlb.inc']
    }
)))

print(json.dumps(
    FauxapiLib.function_call({
        'function': 'return_gateways_status_text',
        'args': [True, False]
    }
)))

print(json.dumps(
    FauxapiLib.function_call({
        'function': 'get_carp_status',
    }
)))

print(json.dumps(
    FauxapiLib.function_call({
        'function': 'get_dns_servers',
    }
)))

# NB: this can take sometime to return since it makes an external lookup call itself
# print(json.dumps(
#     FauxapiLib.function_call({
#         'function': 'get_system_pkg_version',
#     }
# )))

print(json.dumps(
    FauxapiLib.function_call({
        'function': 'pkg_list_repos',
    }
)))

print(json.dumps(
    FauxapiLib.function_call({
        'function': 'get_services',
    }
)))

print(json.dumps(
    FauxapiLib.function_call({
        'function': 'get_service_status',
        'args': ['ntpd']
    }
)))

print(json.dumps(
    FauxapiLib.function_call({
        'function': 'is_service_enabled',
        'args': ['ntpd']
    }
)))

print(json.dumps(
    FauxapiLib.function_call({
        'function': 'is_service_running',
        'args': ['ntpd']
    }
)))

# system_info
# =============================================================================
print(json.dumps(
    FauxapiLib.system_info())
)
